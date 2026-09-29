#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 FI-CTRL-001" >&2
    exit 2
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
FAULT_ID="$1"
FAULT_DIR="$REPO_ROOT/fault_injection/autoware/$FAULT_ID"

if [[ ! -f "$FAULT_DIR/Dockerfile" ]]; then
    echo "Unknown Autoware fault: $FAULT_ID" >&2
    exit 2
fi

IMAGE_TAG="autoware-cctest-fault:${FAULT_ID,,}"
docker build --tag "$IMAGE_TAG" "$FAULT_DIR"
echo "$IMAGE_TAG"
