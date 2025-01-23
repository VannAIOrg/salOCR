import streamlit as st
import numpy as np
import cv2
import os
from pdf_utils import extract_page, process_pdf
from image_utils import preprocess_image, find_large_contours, mask_large_areas
from text_utils import extract_text_from_regions

# Streamlit I user interface
st.title("salOCR - Hindi PDF Text Extraction")
st.sidebar.header("Options")
dpi= 300

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file temporarily
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Select Page for Processing
    st.subheader("Select a Page to Process")
    pages = extract_page(file_path, 1, dpi=dpi)
    total_pages = len(pages)
    page_num = st.slider("Page Number", 1, total_pages, 1)
    page_image = extract_page(file_path, page_num, dpi=dpi)

    # Display Input Image
    st.image(page_image, caption=f"Original Page {page_num}", use_container_width=True)

    # Process Image
    st.subheader("Processing Image...")
    binary_image = preprocess_image(page_image)
    large_contours = find_large_contours(binary_image)
    masked_image = mask_large_areas(binary_image, large_contours)

    # Display Processed Image
    st.image(masked_image, caption="Processed Image", use_container_width=True)

    # Extract Text
    st.subheader("Extracted Text")
    text_regions = find_large_contours(masked_image)
    extracted_text = extract_text_from_regions(page_image, text_regions, language="hin")
    st.text_area("Extracted Text", extracted_text, height=300)

    # Save Results
    if st.button("Save Extracted Text"):
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{uploaded_file.name}_page_{page_num}.txt")
        with open(output_path, "w", encoding="utf-8") as text_file:
            text_file.write(extracted_text)
        st.success(f"Text saved successfully at {output_path}!")
