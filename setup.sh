#!/bin/bash

# Setup script for Rutiranje project on Linux/macOS
# Installs all required dependencies

echo "=========================================="
echo "Rutiranje - Python 3 Setup"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Detected: $PYTHON_VERSION"
echo ""

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies from requirements.txt..."
python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ All dependencies installed successfully!"
    echo "=========================================="
    echo ""
    echo "You can now run the program with:"
    echo "  python3 main.py"
    echo ""
    echo "=========================================="
else
    echo ""
    echo "✗ Installation failed"
    exit 1
fi
