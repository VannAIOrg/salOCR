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

def extract_text_from_contours(image, contours,language='hin'):
    """Extract text from each contour region."""
    extracted_texts = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        region = image[y:y+h, x:x+w]
        text = pytesseract.image_to_string(region, config='--psm 6',lang=language)
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

        # Extract all pages
        pages = pdf2image.convert_from_path(file_path)
        total_pages = len(pages)

        st.write(f"Total Pages in PDF: {total_pages}")
        page_data = []

        # Process all pages
        for page_num in range(1, total_pages + 1):
            page_image = extract_page(file_path, page_num)
            binary_image = preprocess_image(page_image)

            # Kernel parameters
            kernel_width = 50
            kernel_height = 100
            kernel = np.ones((kernel_height, kernel_width), np.uint8)
            closed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

            # Find contours and extract OCR
            min_area = 10000  # Fixed or adjustable
            large_contours = find_large_contours(closed_image, min_area)
            image_with_contours = draw_contours(page_image, large_contours)
            masked_image = mask_large_areas(binary_image, large_contours)

            # OCR for each contour
            ocr_results = []
            for i, contour in enumerate(large_contours):
                x, y, w, h = cv2.boundingRect(contour)
                region = page_image[y:y + h, x:x + w]
                text = pytesseract.image_to_string(region, config='--psm 6',lan='hin')
                ocr_results.append(f"Region {i + 1}: {text.strip()}")

            # Store data for the page
            page_data.append({
                "page_num": page_num,
                "binary_image": binary_image,
                "image_with_contours": image_with_contours,
                "masked_image": masked_image,
                "ocr_results": ocr_results,
            })

        # Display processed images for the first page
        st.subheader("Processed Images (First Page)")
        first_page_data = page_data[0]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(first_page_data["binary_image"], caption="Binary Image (Page 1)", use_container_width=True, clamp=True)
        with col2:
            st.image(first_page_data["image_with_contours"], caption="Contours on Original Image (Page 1)", use_container_width=True)
        with col3:
            st.image(first_page_data["masked_image"], caption="Masked Image (Page 1)", use_container_width=True)

        # Display OCR results for all pages
        st.subheader("OCR Results for All Pages")
        for page in page_data:
            with st.expander(f"Page {page['page_num']} OCR Results"):
                for result in page["ocr_results"]:
                    st.write(result)


if __name__ == "__main__":
    main()
