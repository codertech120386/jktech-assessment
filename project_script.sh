#!/bin/bash

# Exit the script if any command fails
set -e

echo "Starting ollama..."
nohup ollama start &
sleep 10

# Starting Uvicorn
uvicorn main:app --host 0.0.0.0 --port 80