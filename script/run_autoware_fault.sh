#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 FI-CTRL-001" >&2
    exit 2
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
FAULT_ID="$1"
IMAGE_TAG="autoware-cctest-fault:${FAULT_ID,,}"

if ! docker image inspect "$IMAGE_TAG" >/dev/null 2>&1; then
    echo "Fault image not found: $IMAGE_TAG" >&2
    echo "Build it first with: script/build_autoware_fault.sh $FAULT_ID" >&2
    exit 2
fi

AUTOWARE_IMAGE="$IMAGE_TAG" exec "$SCRIPT_DIR/run_autoware.sh" v1
