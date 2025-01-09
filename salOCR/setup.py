## Run this file to install all dependencies and relavant libraries used in main.py

import subprocess
import sys

# List of dependencies
dependencies = [
    "opencv-python",
    "numpy",
    "pdf2image",
    "pytesseract"
]

# Install all dependencies

def install_packages():
    for package in dependencies:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {str(e)}")

if __name__ == "__main__":
    install_packages()
