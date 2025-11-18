#!/bin/bash
# Quick start script for Linux/Mac

echo "Starting Research Assistant AI..."
echo

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found at venv/"
    echo "Run: python -m venv venv"
    echo "Then: source venv/bin/activate"
    echo "Then: pip install -r requirements.txt"
    echo
fi

# Start the server
python main.py
