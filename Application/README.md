# salOCR: Hindi PDF Text Extraction  web Application
This is a proof of concept web application for the [salOCR](https://github.com/VannAIOrg/salOCR) repository.

The [website](https://salocr.streamlit.app/)
## Key Additions in Streamlit Application

### Major updates
- Interactive web interface using Streamlit.
- Dynamic PDF processing with visualization of processing steps.
- Enhanced text region detection and visualization.
- Comprehensive OCR results display, page wise and consolidated.
- Per-page and consolidated text extraction.
- Download functionality for extracted text.

### Technical Enhancements
- Morphological operations for text region segmentation
- Customizable contour detection parameters
- Multi-page PDF processing
- Visualization of:
  - Binary images
  - Contour-highlighted pages
  - Region-wise OCR results

## Features
- Web-based PDF processing
- Supports multiple page PDFs
- Displays processing stages
- Exports extracted text
- Uses Pytesseract for Hindi OCR

## Example output

![example page2 jpg](https://github.com/user-attachments/assets/841eeafa-2569-46a7-ab8c-eee8058d46db)
![example page2(Boxed)](https://github.com/user-attachments/assets/29eefee0-c68b-4323-b0ec-cb7e587c4d67)
![Uploading binary.jpg…]()


## Installation
```bash
pip install streamlit opencv-python pytesseract pdf2image
```

## Usage
```bash
streamlit run app.py
```

## Recommended Future Improvements
- Implement YOLO for advanced text region detection, to speed up the processing required for textual region detectection.
- Improve error handling, with more granular segmentation of text,images and illustrated regions, possibly use a DeepLearning model for those regions.
