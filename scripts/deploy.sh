#!/bin/bash

set -euo pipefail

readonly SCRIPT_NAME="$( basename "${BASH_SOURCE[0]}" )"
readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
readonly REPO_DIR="$( dirname "$( dirname "${SCRIPT_DIR}" )" )"
readonly SOURCE_BRANCH="ap-initial-backend"
readonly PREFIX_DIR="fzw-backend"

log () {
    echo "[${SCRIPT_NAME}] $1"
}

main () {
    local split_hash=""
    log "Entering ${REPO_DIR}"
    cd "${REPO_DIR}"

    split_hash=$( git subtree split --prefix "${PREFIX_DIR}" "${SOURCE_BRANCH}" )
    log "Prefix commit hash generated: ${split_hash}"
    git push heroku "${split_hash}:refs/heads/master" --force
    log "Deploy successful"
}

main
