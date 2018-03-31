#!/bin/bash

set -euo pipefail

pylint --rcfile=setup.cfg fzw -E "$@"
