import platform
import sys
import importlib
import pkg_resources  # For checking the version of pdf2image
import cv2
import numpy as np
import pdf2image
import pytesseract

def get_library_version(library_name):
    try:
        if library_name == "pdf2image":
            # Special handling for pdf2image version
            return pkg_resources.get_distribution("pdf2image").version
        lib = importlib.import_module(library_name)
        return getattr(lib, '__version__', 'Unknown version')
    except ImportError:
        return 'Not installed'

def get_system_info():
    info = "----------------------------------------\n"
    info += "System information\n"
    info += "----------------------------------------\n"
    info += f"Platform:      {platform.platform()}\n"
    info += f"Python:        {platform.python_version()}\n"
    info += f"NumPy:         {get_library_version('numpy')}\n"
    info += f"OpenCV:        {get_library_version('cv2')}\n"
    info += f"pdf2image:     {get_library_version('pdf2image')}\n"
    info += f"pytesseract:   {get_library_version('pytesseract')}\n"
    return info

if __name__ == "__main__":
    print(get_system_info())