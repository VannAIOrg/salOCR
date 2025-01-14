import cv2
import numpy as np
import pdf2image
import pytesseract
import os
from tqdm import tqdm
from joblib import Parallel, delayed  # For parallel processing

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

def save_text(folder_path, filename, text):
    """Save extracted text to a file in the specified folder."""
    os.makedirs(folder_path, exist_ok=True)
    output_path = os.path.join(folder_path, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved: {output_path}")
    return output_path

def process_pdf(pdf_path):
    """Process a single PDF and extract text from all pages."""
    print(f"Processing: {os.path.basename(pdf_path)}")
    extracted_text = ""
    try:
        pages = pdf2image.convert_from_path(pdf_path, dpi=300, grayscale=True)
        total_pages = len(pages)
        for page_number, page in enumerate(pages, start=1):
            page_array = np.array(page)
            binary_page = preprocess_image(page_array)

            # Mask large areas like tables
            large_contours = find_large_contours(binary_page)
            masked_image = mask_large_areas(binary_page, large_contours)

            # Extract text outside tables
            text_regions = get_text_regions(masked_image)
            outside_text = extract_text_from_regions(page_array, text_regions)
            extracted_text += f"\n--- Page {page_number}: Outside Tables ---\n{outside_text}\n"

            # Extract text inside tables
            for idx, table in enumerate(large_contours, start=1):
                x, y, w, h = cv2.boundingRect(table)
                table_region = page_array[y:y + h, x:x + w]
                table_text_regions = get_text_regions(preprocess_image(table_region))
                table_text = extract_text_from_regions(table_region, table_text_regions)
                extracted_text += f"\n--- Page {page_number}: Table {idx} ---\n{table_text}\n"
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
    return os.path.basename(pdf_path), extracted_text

def main():
    pdf_folder = "HindiBooks"  # Folder containing PDF files
    output_folder = os.path.join(pdf_folder, "combined_text")
    combined_text_path = os.path.join(output_folder, "combined_text.txt")

    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    total_pdfs = len(pdf_files)

    # Process PDFs in parallel
    results = Parallel(n_jobs=-1)(
        delayed(process_pdf)(pdf_path) for pdf_path in pdf_files
    )

    # Combine text from all PDFs
    all_text = ""
    pdf_names = []
    for pdf_name, pdf_text in results:
        all_text += f"\n--- {pdf_name} ---\n{pdf_text}\n"
        pdf_names.append(pdf_name)

    save_text(output_folder, "combined_text.txt", all_text)

    # Summary
    word_count = len(all_text.split())
    print("\n--- Processing Complete ---")
    print(f"Total PDFs processed: {total_pdfs}")
    print(f"PDF Names: {', '.join(pdf_names)}")
    print(f"Total word count: {word_count}")

if __name__ == "__main__":
    main()
