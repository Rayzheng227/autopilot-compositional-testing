#!/usr/bin/env python3
"""Add function/code-level fault ground truth to existing recorded scenes."""

import argparse
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "fault_injection" / "autoware" / "catalog.yaml"
GT_KEYS = (
    "id", "module", "package", "source_file", "function", "injection_point",
    "mutation", "code_change", "parameters", "activation_condition",
    "activation_oracle", "expected_responsibility", "responsibility_basis",
)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("recording_root", type=Path)
    args = parser.parse_args()

    catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
    faults = {item["id"]: item for item in catalog["faults"]}
    updated = 0
    skipped = 0
    for scene_path in sorted(args.recording_root.rglob("scene.yaml")):
        fault_id = next((part for part in scene_path.parts if part in faults), None)
        if not fault_id or not faults[fault_id].get("patch_file"):
            skipped += 1
            continue
        fault = faults[fault_id]
        ground_truth = {key: fault[key] for key in GT_KEYS if key in fault}
        ground_truth["patch_file"] = str(REPO_ROOT / fault["patch_file"])
        document = yaml.safe_load(scene_path.read_text(encoding="utf-8")) or {}
        document["GroundTruth"] = ground_truth
        scene_path.write_text(
            yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding="utf-8"
        )
        updated += 1
    print(f"updated={updated} skipped={skipped}")


if __name__ == "__main__":
    main()
