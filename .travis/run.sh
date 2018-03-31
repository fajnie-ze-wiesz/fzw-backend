#!/bin/bash

set -euo pipefail

readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
readonly SCRIPT_NAME="$( basename "${BASH_SOURCE[0]}" )"
readonly BASE_DIR="$( dirname "${SCRIPT_DIR}" )"

print_step() {
    echo ""
    echo "[${SCRIPT_NAME}] $1"
}

main() {
    print_step "Running flake8"
    flake8 .
    print_step "Running isort"
    isort --check
    print_step "Running pylint"
    "${BASE_DIR}/scripts/run_pylint.sh"
}

main
