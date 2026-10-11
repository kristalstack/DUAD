#!/usr/bin/env bash
set -euo pipefail
python -m pytest | tee test-report.txt
