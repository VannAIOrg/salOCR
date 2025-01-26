from setuptools import setup, find_packages

setup(
    name="salOCR",
    version="1.0",
    description="An application for Hindi PDF text extraction using OCR.",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "opencv-python",
        "numpy",
        "pytesseract",
        "pdf2image",
        "joblib",
        "tqdm"
    ],
    python_requires=">=3.7"
)
