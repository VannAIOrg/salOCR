import pdf2image
import numpy as np

def extract_page(file_path, page_num, dpi=300):
    pages = pdf2image.convert_from_path(file_path, first_page=page_num, last_page=page_num, dpi=dpi, grayscale=True)
    return np.array(pages[0])

def process_pdf(pdf_path, image_utils, text_utils):
    print(f"Processing: {os.path.basename(pdf_path)}")
    extracted_text = ""
    try:
        pages = pdf2image.convert_from_path(pdf_path, dpi=300, grayscale=True)
        total_pages = len(pages)
        for page_number, page in enumerate(pages, start=1):
            page_array = np.array(page)
            binary_page = image_utils.preprocess_image(page_array)

            large_contours = image_utils.find_large_contours(binary_page)
            masked_image = image_utils.mask_large_areas(binary_page, large_contours)

            text_regions = image_utils.get_text_regions(masked_image)
            outside_text = text_utils.extract_text_from_regions(page_array, text_regions)
            extracted_text += f"\n--- Page {page_number}: Outside Tables ---\n{outside_text}\n"

            for idx, table in enumerate(large_contours, start=1):
                x, y, w, h = cv2.boundingRect(table)
                table_region = page_array[y:y + h, x:x + w]
                table_text_regions = image_utils.get_text_regions(image_utils.preprocess_image(table_region))
                table_text = text_utils.extract_text_from_regions(table_region, table_text_regions)
                extracted_text += f"\n--- Page {page_number}: Table {idx} ---\n{table_text}\n"
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
    return os.path.basename(pdf_path), extracted_text
