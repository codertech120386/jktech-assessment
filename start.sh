#!/bin/bash

# Exit the script if any command fails
set -e

echo "Starting ollama..."
nohup ollama start &
sleep 10
echo "ollama Started"
ollama pull llama3


