import streamlit as st
import numpy as np
import cv2
import os
import pdf2image
from image_utils import preprocess_image, find_large_contours, mask_large_areas, get_text_regions
from text_utils import extract_text_from_regions

def process_page(page_image, page_num):
    """
    Process a single page
    
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
st.title("salOCR - Single-Page Hindi PDF Text Extraction")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # Save temporary file
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Convert first PDF page to image
    pages = pdf2image.convert_from_path(file_path, first_page=1, last_page=1)
    if pages:
        page_image = np.array(pages[0])
        
        # Process the first page
        result = process_page(page_image, 1)
        
        if result:
            st.subheader(f"Page 1 Results")
            
            # Original Image
            st.image(result['original_image'], caption="Original Page 1", use_container_width=True)
            
            # Bounding Boxes
            boxed_image = draw_bounding_boxes(result['original_image'], result['contours'])
            st.image(boxed_image, caption="Detected Regions", use_container_width=True)
            
            # Masked Image
            st.image(result['masked_image'], caption="Processed Image", use_container_width=True)
            
            # Extracted Text
            st.text_area("Extracted Text", result['extracted_text'], height=200)
            
            # Download Option
            if st.button("Download Extracted Text"):
                output_dir = "output"
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"{uploaded_file.name}_page_1_text.txt")
                with open(output_path, "w", encoding="utf-8") as text_file:
                    text_file.write(result['extracted_text'])
                st.success(f"Text saved successfully at {output_path}!")
        else:
            st.error("Failed to process the page.")
    else:
        st.error("No pages found in the PDF.")
else:
    st.info("Please upload a PDF file.")
