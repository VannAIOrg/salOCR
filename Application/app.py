import cv2
import numpy as np
import pdf2image
import os
import streamlit as st
from image_utils import preprocess_image, find_large_contours, mask_large_areas
import pytesseract

def extract_page(file_path, page_num, dpi=300):
    """Extract a specific page from PDF."""
    pages = pdf2image.convert_from_path(file_path, first_page=page_num, last_page=page_num, dpi=dpi, grayscale=True)
    return np.array(pages[0])

def draw_contours(image, contours):
    """Draw contours on the image for visualization."""
    image_with_contours = image.copy()
    cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)
    return image_with_contours

def extract_text_from_contours(image, contours):
    """Extract text from each contour region."""
    extracted_texts = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        region = image[y:y+h, x:x+w]
        text = pytesseract.image_to_string(region, config='--psm 6')
        extracted_texts.append((f"Region {i+1}", text.strip()))
    return extracted_texts

def main():
    st.title("salOCR - Debugging Contours")

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
        st.image(page_image, caption=f"Original Page {page_num}", use_container_width=True)

        # Process Image
        st.subheader("Processing Image...")
        binary_image = preprocess_image(page_image)

        # Kernel parameters fixed
        kernel_width = 50
        kernel_height = 100
        kernel = np.ones((kernel_height, kernel_width), np.uint8)
        
        closed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

        # Find and visualize large contours
        min_area = st.sidebar.slider("Minimum Contour Area", 5000, 50000, 10000, step=1000)
        large_contours = find_large_contours(closed_image, min_area)

        image_with_contours = draw_contours(page_image, large_contours)
        masked_image = mask_large_areas(binary_image, large_contours)

        # Display images side by side
        st.subheader("Processed Images")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(binary_image, caption="Binary Image", use_container_width=True, clamp=True)
        with col2:
            st.image(image_with_contours, caption="Contours on Original Image", use_container_width=True)
        with col3:
            st.image(masked_image, caption="Masked Image", use_container_width=True, clamp=True)

        # Extract and Display OCR Results for each contour
        st.subheader("OCR Results")
        ocr_results = extract_text_from_contours(page_image, large_contours)
        for region_name, text in ocr_results:
            st.write(f"**{region_name}:**")
            st.text_area("Extracted Text", text, height=100)

        # Debug Output
        st.subheader("Debugging Output")
        st.write(f"Number of Contours Found: {len(large_contours)}")

if __name__ == "__main__":
    main()
