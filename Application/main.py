from joblib import Parallel, delayed
import os
from pdf_utils import process_pdf
from image_utils import preprocess_image, find_large_contours, mask_large_areas, get_text_regions
from text_utils import extract_text_from_regions, save_text

def main():
    pdf_folder = "HindiBooks"
    output_folder = os.path.join(pdf_folder, "combined_text")
    combined_text_path = os.path.join(output_folder, "combined_text.txt")

    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    total_pdfs = len(pdf_files)

    # Process PDFs in parallel
    results = Parallel(n_jobs=1)(
        delayed(process_pdf)(pdf_path, image_utils, text_utils) for pdf_path in pdf_files
    )

    # Combine text from all PDFs
    all_text = ""
    pdf_names = []
    for pdf_name, pdf_text in results:
        all_text += f"\n--- {pdf_name} ---\n{pdf_text}\n"
        pdf_names.append(pdf_name)

    save_text(output_folder, "combined_text.txt", all_text)

    word_count = len(all_text.split())
    print("\n--- Processing Complete ---")
    print(f"Total PDFs processed: {total_pdfs}")
    print(f"PDF Names: {', '.join(pdf_names)}")
    print(f"Total word count: {word_count}")

if __name__ == "__main__":
    main()
