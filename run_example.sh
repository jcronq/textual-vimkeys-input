#!/bin/bash
# Helper script to run examples with virtual environment

# Activate .venv
source .venv/bin/activate

# Run the example passed as argument
if [ -z "$1" ]; then
    echo "Usage: ./run_example.sh <example_name>"
    echo "Examples:"
    echo "  ./run_example.sh 01_spike"
    echo "  ./run_example.sh 02_simple_chat"
    echo "  ./run_example.sh 03_streaming_chat"
    exit 1
fi

python examples/${1}.py
