from PIL import Image
import pytesseract

def extract_text_with_ocr(file_path):
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error reading image {file_path}: {e}")
        return ""
