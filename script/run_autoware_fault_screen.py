#!/usr/bin/env python3
"""Run a deterministic fault-screen batch with one rosbag per case."""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
CASE_ATTEMPTS = 3
sys.path.insert(0, str(REPO_ROOT / "tools" / "autoware-control-panel"))
from server import MANAGER  # noqa: E402


def case_name(fault_id, case):
    values = [fault_id, case["vista"], f"ve-{case['ve']}", f"xf-{case['xf']}"]
    if "xa" in case:
        values.append(f"xa-{case['xa']}")
    return "_".join(values).replace(".", "p")


def load_ground_truth(fault_id):
    catalog_path = REPO_ROOT / "fault_injection" / "autoware" / "catalog.yaml"
    catalog = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    fault = next(item for item in catalog["faults"] if item["id"] == fault_id)
    keys = (
        "id", "module", "package", "source_file", "function", "injection_point",
        "mutation", "code_change", "parameters", "activation_condition",
        "activation_oracle", "expected_responsibility", "responsibility_basis",
    )
    ground_truth = {key: fault[key] for key in keys if key in fault}
    if fault.get("patch_file"):
        ground_truth["patch_file"] = str(REPO_ROOT / fault["patch_file"])
    return ground_truth


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_file", type=Path)
    parser.add_argument("--no-record", action="store_true")
    args = parser.parse_args()

    config = json.loads(args.batch_file.read_text(encoding="utf-8"))
    fault_id = config["fault_id"]
    ground_truth = load_ground_truth(fault_id)
    cases = config["cases"]
    recording_template = config.get("recording", {})
    output_root = REPO_ROOT / "test_result" / "fault_injection" / fault_id
    output_root.mkdir(parents=True, exist_ok=True)
    summary_path = output_root / "summary.jsonl"

    for index, case in enumerate(cases, start=1):
        name = case_name(fault_id, case)
        result_path = output_root / case["vista"] / f"ve={case['ve']:g}" / f"{name}.json"
        if result_path.exists():
            print(f"[{index}/{len(cases)}] skip {name}", flush=True)
            continue

        recording_started = False
        if recording_template.get("enabled", True) and not args.no_record:
            recording = dict(recording_template)
            recording["name"] = name
            recording["scene"] = dict(case)
            ok, message = MANAGER.start_recording(recording)
            if not ok:
                raise RuntimeError(message)
            recording_started = True

        command = [
            str(REPO_ROOT / "script/run_single.sh"), "autoware", case["vista"],
            "-ve", str(case["ve"]), "-xf", str(case["xf"]), "--json",
        ]
        if case["vista"] != "crossing_with_traffic_lights":
            command.extend(["-xa", str(case["xa"])])
        print(f"[{index}/{len(cases)}] run {name}", flush=True)
        try:
            result = None
            last_error = None
            for attempt in range(1, CASE_ATTEMPTS + 1):
                try:
                    completed = subprocess.run(
                        command, cwd=REPO_ROOT, capture_output=True, text=True,
                        timeout=300, check=True,
                    )
                    result = json.loads(completed.stdout)
                    break
                except (subprocess.SubprocessError, json.JSONDecodeError) as error:
                    last_error = error
                    if attempt == CASE_ATTEMPTS:
                        raise RuntimeError(
                            f"{name} produced no verdict after {CASE_ATTEMPTS} attempts: {error}"
                        ) from error
                    print(
                        f"[{index}/{len(cases)}] no verdict; retry "
                        f"{attempt + 1}/{CASE_ATTEMPTS}", flush=True,
                    )
                    time.sleep(3)
            if result is None:
                raise RuntimeError(f"{name} did not produce a result: {last_error}")
            verdict = result["verdict"]
            scene = {
                **case, "verdict": verdict, "fault_id": fault_id,
                "ground_truth": ground_truth,
            }
            if recording_started:
                ok, message = MANAGER.stop_recording("v1", save=True, scene=scene)
                if not ok:
                    raise RuntimeError(message)
            result.update({"fault_id": fault_id, "source_verdict": case.get("source_verdict")})
            result_path.parent.mkdir(parents=True, exist_ok=True)
            result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
            with summary_path.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps({**case, "fault_verdict": verdict}) + "\n")
            print(f"[{index}/{len(cases)}] {case.get('source_verdict')} -> {verdict}", flush=True)
        except Exception:
            if recording_started and MANAGER.recordings.get("v1"):
                MANAGER.stop_recording("v1", save=False)
            raise
        time.sleep(2)


if __name__ == "__main__":
    main()
