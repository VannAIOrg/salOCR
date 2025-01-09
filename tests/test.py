## Use this python file to test a single page of your PDF to assess the results before bulk processing of PDFs in the main.py file (in salOCR directory)
## The output file will be saved in your project folder after processing
## A sample PDF 'AnimalFarm-Hindi' can be used for this testing, or you can add your own PDF file and change the 'input_pdf' file name accordingly

import cv2
import numpy as np
import pdf2image
import pytesseract
import os



def main():
    # File paths and page number
    input_pdf = 'AnimalFarm-Hindi.pdf' # Input PDF file stored in the 'tests' directory
    page_number = 34

    # Step 1: Extract and preprocess the page
    page = extract_page(input_pdf, page_number)
    binary_page = preprocess_image(page)

    # Step 2: Detect and mask large areas (e.g., tables)
    large_contours = find_large_contours(binary_page)
    masked_image = mask_large_areas(binary_page, large_contours)

    # Step 3: Extract text outside tables
    text_regions = get_text_regions(masked_image)
    outside_text = extract_text_from_regions(page, text_regions)
    outside_text_path = save_text("AnimalFarm_34.txt", outside_text)
    print(f"Text Outside Tables saved at: {outside_text_path}")

    # Step 4: Extract text inside tables
    for idx, table in enumerate(large_contours, start=1):
        x, y, w, h = cv2.boundingRect(table)
        table_region = page[y:y + h, x:x + w]
        table_text_regions = get_text_regions(preprocess_image(table_region))
        table_text = extract_text_from_regions(table_region, table_text_regions)
        table_text_path = save_text(f"table_{idx}_text.txt", table_text)
        print(f"Text Inside Table {idx} saved at: {table_text_path}")

def extract_page(file_path, page_num, dpi=300):
    """Convert a specific page of a PDF to a numpy array."""
    pages = pdf2image.convert_from_path(file_path, first_page=page_num, last_page=page_num, dpi=dpi, grayscale=True)
    return np.array(pages[0])


def preprocess_image(image):
    """Apply thresholding to prepare the image for contour detection."""
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    return binary_image


def find_large_contours(image, min_area=10000):
    """Find large contours based on the area."""
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]


def mask_large_areas(image, contours):
    """Mask out large areas like tables."""
    mask = image.copy()
    cv2.drawContours(mask, contours, -1, 0, thickness=cv2.FILLED)
    return mask


def get_text_regions(image):
    """Detect text regions by closing gaps between contours."""
    kernel = np.ones((20, 50), np.uint8)
    closed_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return sorted([cv2.boundingRect(c) for c in contours], key=lambda r: r[1])


def extract_text_from_regions(image, regions, language='hin'):
    """Extract text from specific regions."""
    text_output = ""
    for x, y, w, h in regions:
        roi = image[y:y + h, x:x + w]
        text = pytesseract.image_to_string(roi, config='--psm 6', lang=language)
        text_output += text.strip() + "\n"
    return text_output


def save_text(filename, text):
    """Save extracted text to a file in the project folder."""
    project_folder = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_folder, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved: {output_path}")
    return output_path



if __name__ == "__main__":
    main()
