import streamlit as st
import numpy as np
import cv2
import os
import pdf2image
from image_utils import preprocess_image, find_large_contours, mask_large_areas, get_text_regions
from text_utils import extract_text_from_regions

def extract_page(file_path, page_num, dpi=300):
    """Extract a specific page from PDF"""
    pages = pdf2image.convert_from_path(file_path, first_page=page_num, last_page=page_num, dpi=dpi, grayscale=True)
    return np.array(pages[0])

def draw_bounding_boxes(image, contours):
    """Draw bounding boxes on the image for detected contours"""
    boxed_image = image.copy()
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(boxed_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return boxed_image

# Streamlit user interface
st.title("salOCR ")
st.write("Hindi PDF Text Extraction tool")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file temporarily
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Determine total pages
    pages = pdf2image.convert_from_path(file_path)
    total_pages = len(pages)
    
    # Select Page for Processing
    st.subheader("Select a Page to Process")
    page_num = st.slider("Page Number", 1, total_pages, 1)
    
    # Extract specific page
    page_image = extract_page(file_path, page_num)
    
    # Display Input Image
    st.image(page_image, caption=f"Original Page {page_num}", use_container_width=True)
    
    # Process Image
    st.subheader("Processing Image...")
    binary_image = preprocess_image(page_image)
    large_contours = find_large_contours(binary_image)
    
    # Draw bounding boxes on the original image
    boxed_image = draw_bounding_boxes(page_image, large_contours)
    st.image(boxed_image, caption="Detected Regions with Bounding Boxes", use_container_width=True)
    
    # Mask large areas
    masked_image = mask_large_areas(binary_image, large_contours)
    st.image(masked_image, caption="Processed Image", use_container_width=True)
    
    # Extract Text from Regions
    st.subheader("Extracted Text")
    text_regions = get_text_regions(masked_image)
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
