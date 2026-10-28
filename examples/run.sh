#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src python -m gbt_zimage_rewash info
PYTHONPATH=src python -m gbt_zimage_rewash check --payload '{}'
PYTHONPATH=src python -m gbt_zimage_rewash run   --payload '{}'
