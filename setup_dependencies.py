#!/usr/bin/env python3
"""
Setup script for Rutiranje project
Installs all required dependencies for the Vehicle Routing Problem solver
"""

import subprocess
import sys

def install_requirements():
    """Install all required packages from requirements.txt"""
    print("=" * 60)
    print("Rutiranje - Python 3 Setup")
    print("=" * 60)
    print(f"\nPython version: {sys.version}\n")
    
    try:
        print("Installing required packages...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--upgrade", "pip"
        ])
        
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt"
        ])
        
        print("\n" + "=" * 60)
        print("✓ All dependencies installed successfully!")
        print("=" * 60)
        print("\nYou can now run the program with:")
        print("  python3 main.py")
        print("\n" + "=" * 60)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error during installation: {e}")
        return False

if __name__ == "__main__":
    success = install_requirements()
    sys.exit(0 if success else 1)
