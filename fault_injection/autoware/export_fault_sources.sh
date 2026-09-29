#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
output_dir="${1:-$script_dir/exported_sources}"
base_revision="896fd1418b25c1501bad7f9b0116af1c0c8dd941"

mkdir -p "$output_dir"

fault_ids=(FI-CTRL-002 FI-CTRL-003 FI-PLAN-005)
images=(
  autoware-cctest-fault:fi-ctrl-002
  autoware-cctest-fault:fi-ctrl-003
  autoware-cctest-fault:fi-plan-005
)
source_paths=(
  /autoware/src/universe/autoware.universe/control/vehicle_cmd_gate/src/vehicle_cmd_gate.cpp
  /autoware/src/universe/autoware.universe/control/vehicle_cmd_gate/src/vehicle_cmd_gate.cpp
  /autoware/src/universe/autoware.universe/planning/motion_velocity_smoother/src/motion_velocity_smoother_node.cpp
)

manifest="$output_dir/MANIFEST.sha256"
: > "$manifest"

for index in "${!fault_ids[@]}"; do
  fault_id="${fault_ids[$index]}"
  image="${images[$index]}"
  source_path="${source_paths[$index]}"
  destination="$output_dir/$fault_id"
  mkdir -p "$destination"

  if ! docker image inspect "$image" >/dev/null 2>&1; then
    echo "Missing image: $image" >&2
    echo "Build it with: bash script/build_autoware_fault.sh $fault_id" >&2
    exit 1
  fi

  container_id="$(docker create "$image")"
  trap 'docker rm -f "$container_id" >/dev/null 2>&1 || true' EXIT
  docker cp "$container_id:$source_path" "$destination/"
  docker rm "$container_id" >/dev/null
  trap - EXIT

  cp "$script_dir/$fault_id/"*.patch "$destination/"
  cp "$script_dir/$fault_id/Dockerfile" "$destination/"
  cp "$script_dir/$fault_id/README.md" "$destination/"
done

(
  cd "$output_dir"
  find . -type f ! -name 'MANIFEST.sha256' -print0 \
    | sort -z \
    | xargs -0 sha256sum > MANIFEST.sha256
)

printf 'Autoware base revision: %s\n' "$base_revision"
printf 'Exported fault sources: %s\n' "$output_dir"
printf 'Integrity manifest: %s\n' "$manifest"
