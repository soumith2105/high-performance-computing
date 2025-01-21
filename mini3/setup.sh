#!/bin/bash

rm -rf .venv
rm -rf venv
python3 -m venv .venv
source .venv/bin/activate
.venv/bin/pip install -r requirements.txt

echo -e "\n\033[92mSetup complete. Run 'python automate_run.py <SERVER_COUNT>' to run tests\033[0m\n"
