import streamlit as st
import numpy as np
import cv2
import os
import pdf2image
import concurrent.futures
from functools import partial

from image_utils import preprocess_image, find_large_contours, mask_large_areas, get_text_regions
from text_utils import extract_text_from_regions

def process_page(page_image, page_num):
    """
    Process a single page with concurrent execution
    
    Args:
        page_image (numpy.ndarray): Page image
        page_num (int): Page number
    
    Returns:
        dict: Processing results for the page
    """
    try:
        # Process image
        binary_image = preprocess_image(page_image)
        large_contours = find_large_contours(binary_image)
        masked_image = mask_large_areas(binary_image, large_contours)
        
        # Extract text regions
        text_regions = get_text_regions(masked_image)
        extracted_text = extract_text_from_regions(page_image, text_regions, language="hin")
        
        return {
            'page_num': page_num,
            'original_image': page_image,
            'masked_image': masked_image,
            'contours': large_contours,
            'extracted_text': extracted_text
        }
    except Exception as e:
        st.error(f"Error processing page {page_num}: {e}")
        return None

def draw_bounding_boxes(image, contours):
    """Draw bounding boxes on the image for detected contours"""
    boxed_image = image.copy()
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(boxed_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return boxed_image

# Streamlit UI
st.title("salOCR - Multi-Page Hindi PDF Text Extraction")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # Save temporary file
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Convert PDF pages to images
    pages = pdf2image.convert_from_path(file_path)
    total_pages = len(pages)
    
    # Parallel page processing
    with st.spinner(f'Processing {total_pages} pages...'):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            process_func = partial(process_page)
            results = list(executor.map(process_func, 
                                        [np.array(page) for page in pages], 
                                        range(1, total_pages + 1)))
    
    # Filter out None results
    results = [r for r in results if r is not None]
    
    # Display results
    for result in results:
        st.subheader(f"Page {result['page_num']}")
        
        # Original Image
        st.image(result['original_image'], 
                 caption=f"Original Page {result['page_num']}", 
                 use_container_width=True)
        
        # Bounding Boxes
        boxed_image = draw_bounding_boxes(result['original_image'], result['contours'])
        st.image(boxed_image, 
                 caption=f"Page {result['page_num']} - Detected Regions", 
                 use_container_width=True)
        
        # Masked Image
        st.image(result['masked_image'], 
                 caption=f"Page {result['page_num']} - Processed Image", 
                 use_container_width=True)
        
        # Extracted Text
        st.text_area(f"Page {result['page_num']} - Extracted Text", 
                     result['extracted_text'], 
                     height=200)
    
    # Option to save all extracted text
    if st.button("Save All Extracted Text"):
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{uploaded_file.name}_extracted_text.txt")
        
        with open(output_path, "w", encoding="utf-8") as text_file:
            for result in results:
                text_file.write(f"--- Page {result['page_num']} ---\n")
                text_file.write(result['extracted_text'] + "\n\n")
        
        st.success(f"Text saved successfully at {output_path}!")
