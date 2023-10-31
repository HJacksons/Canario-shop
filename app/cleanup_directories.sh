#!/bin/bash

echo "Starting cleanup..."

if [ -d "/app/.pytest_cache" ]; then
    echo "Found .pytest_cache directory. Attempting to remove..."
    rm -rf /app/.pytest_cache
else
    echo ".pytest_cache directory not found."
fi

if [ -d "/app/__pycache__" ]; then
    echo "Found __pycache__ directory. Attempting to remove..."
    rm -rf /app/__pycache__
else
    echo "__pycache__ directory not found."
fi

echo "Cleanup complete."
