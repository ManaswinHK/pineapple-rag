#!/bin/bash

# Ensure the script exits on error
set -e

# Run the python script to pull the model if necessary
python pull_model.py

# Start the FastAPI server
echo "Starting FastAPI server..."
exec uvicorn api.main:app --host 0.0.0.0 --port 8080
