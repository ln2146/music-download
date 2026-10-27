#!/bin/sh
set -eu
skill_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
uv venv --python 3.13 --allow-existing "$skill_dir/.venv"
uv pip install --python "$skill_dir/.venv/bin/python" -r "$skill_dir/requirements.txt"
