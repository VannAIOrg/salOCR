import pytesseract
import os

def extract_text_from_regions(image, regions, language='hin'):
    text_output = ""
    for x, y, w, h in regions:
        roi = image[y:y + h, x:x + w]
        text = pytesseract.image_to_string(roi, config='--psm 6', lang=language)
        text_output += text.strip() + "\n"
    return text_output

def save_text(folder_path, filename, text):
    os.makedirs(folder_path, exist_ok=True)
    output_path = os.path.join(folder_path, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved: {output_path}")
    return output_path
