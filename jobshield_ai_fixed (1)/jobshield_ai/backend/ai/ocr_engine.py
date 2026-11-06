"""
OCR and Computer Vision Preprocessing Engine for JobShield AI.
Extracts text from screenshots of job offers, emails, and chat messages.
Uses Pillow image filtering and EasyOCR / pytesseract with robust fallbacks.
"""
import io
import re
import logging
from PIL import Image, ImageEnhance, ImageFilter

logger = logging.getLogger("jobshield.ocr")

def preprocess_image_for_ocr(image: Image.Image) -> Image.Image:
    """Enhances image contrast and binarizes for superior OCR accuracy."""
    try:
        # Convert to grayscale
        gray = image.convert("L")
        # Increase contrast
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(1.8)
        # Sharpen
        sharpened = enhanced.filter(ImageFilter.SHARPEN)
        return sharpened
    except Exception as e:
        logger.warning(f"Image preprocessing warning: {e}")
        return image

def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extracts text from an uploaded screenshot or document image.
    Tries EasyOCR first, then pytesseract, and provides clean fallbacks.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        processed_img = preprocess_image_for_ocr(image)

        # 1. Try EasyOCR if available
        try:
            import easyocr
            reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            # EasyOCR can accept bytes or numpy array
            import numpy as np
            img_np = np.array(processed_img)
            results = reader.readtext(img_np, detail=0)
            text = " ".join(results).strip()
            if text:
                return text
        except Exception as ocr_err:
            logger.info(f"EasyOCR skipped or not initialized: {ocr_err}")

        # 2. Try pytesseract if available
        try:
            import pytesseract
            text = pytesseract.image_to_string(processed_img)
            if text and text.strip():
                return text.strip()
        except Exception as pytess_err:
            logger.info(f"PyTesseract skipped or not installed: {pytess_err}")

        # 3. Fallback: Extract embedded EXIF/metadata or return meaningful note
        # Check if the image has text metadata
        metadata_text = []
        info = image.info
        for k, v in info.items():
            if isinstance(v, str) and len(v) > 10:
                metadata_text.append(v)

        if metadata_text:
            return " ".join(metadata_text)

        return (
            "Offer letter screenshot uploaded successfully. "
            "Please paste the text directly into the AI Text Scanner if automated OCR is not enabled on this host."
        )

    except Exception as e:
        logger.error(f"Error reading image: {e}")
        return f"Image processing error: {str(e)}"
