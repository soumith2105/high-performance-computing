#!/bin/bash

rm -rf .venv
rm -rf venv
python3 -m venv .venv
source .venv/bin/activate
.venv/bin/pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./src/star/grpc/star_service.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./src/ring/grpc/ring.proto

echo -e "\n\033[92mSetup complete. Run 'python main.py <TOPOLOGY>' to run tests\033[0m\nTopology options: RING, STAR (ALL CAPS)\n"
