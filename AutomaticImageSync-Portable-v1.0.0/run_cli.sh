#!/bin/bash
# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Setting up environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

python3 cli.py "$@"
