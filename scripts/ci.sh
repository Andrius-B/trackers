#!/bin/bash
set -e
set -u
set -o pipefail
set -x

poetry run pytest
poetry run mypy trackers tests
poetry run black trackers tests --check