import pdfplumber
from fastapi import UploadFile, HTTPException
from io import BytesIO
import pytesseract
from pdf2image import convert_from_bytes
import os

# Configure Tesseract OCR path for Windows
TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Tesseract-OCR\tesseract.exe",
]

for path in TESSERACT_PATHS:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        break

# Configure Poppler path for Windows (pdf2image)
POPPLER_PATHS = [
    r"C:\poppler\bin",
    r"C:\Program Files\poppler\bin",
    r"C:\poppler-24.08.0\Library\bin",
]

POPPLER_PATH = None
for path in POPPLER_PATHS:
    if os.path.exists(path):
        POPPLER_PATH = path
        break


async def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Extract text from uploaded PDF file.
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        Extracted plain text from the PDF
        
    Raises:
        HTTPException: If file is corrupted or not a valid PDF
    """
    try:
        contents = await file.read()
        pdf_bytes = BytesIO(contents)
        
        text_content = []
        
        with pdfplumber.open(pdf_bytes) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
        
        full_text = "\n".join(text_content)
        
        # Clean up the text
        full_text = clean_text(full_text)
        
        # If no text extracted, try OCR for image-based PDFs
        if not full_text.strip():
            full_text = extract_text_with_ocr(contents)
        
        if not full_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF. The file may be empty or OCR failed."
            )
        
        return full_text
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse PDF: {str(e)}. The file may be corrupted or not a valid PDF."
        )


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing excess whitespace and normalizing.
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Replace multiple spaces with single space
    import re
    text = re.sub(r' +', ' ', text)
    
    # Replace multiple newlines with double newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    return text.strip()


def extract_text_with_ocr(pdf_bytes: bytes) -> str:
    """
    Extract text from image-based PDF using OCR.
    
    Args:
        pdf_bytes: PDF file as bytes
        
    Returns:
        Extracted text using OCR
    """
    try:
        # Convert PDF pages to images
        if POPPLER_PATH:
            images = convert_from_bytes(pdf_bytes, dpi=300, poppler_path=POPPLER_PATH)
        else:
            images = convert_from_bytes(pdf_bytes, dpi=300)
        
        text_content = []
        for image in images:
            # Run OCR on each page image
            page_text = pytesseract.image_to_string(image)
            if page_text:
                text_content.append(page_text)
        
        return clean_text("\n".join(text_content))
        
    except Exception as e:
        # OCR failed, return empty string to trigger the error message
        print(f"OCR extraction failed: {str(e)}")
        return ""


def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF bytes directly (synchronous version).
    
    Args:
        pdf_bytes: PDF file as bytes
        
    Returns:
        Extracted plain text
    """
    try:
        pdf_buffer = BytesIO(pdf_bytes)
        text_content = []
        
        with pdfplumber.open(pdf_buffer) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
        
        full_text = clean_text("\n".join(text_content))
        
        # Try OCR if no text extracted
        if not full_text.strip():
            full_text = extract_text_with_ocr(pdf_bytes)
        
        return full_text
        
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")
