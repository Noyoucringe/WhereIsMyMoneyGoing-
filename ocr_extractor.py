"""
OCR Extractor Module
Extracts text from bank statements (PDFs and images) using Tesseract OCR
"""

import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import PyPDF2
from typing import List, Optional
import io


class OCRExtractor:
    """Extract text from various document formats"""
    
    def __init__(self, tesseract_path: Optional[str] = None):
        """
        Initialize OCR extractor
        
        Args:
            tesseract_path: Path to tesseract executable (optional)
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    def extract_from_image(self, image_path: str, lang: str = 'eng') -> str:
        """
        Extract text from an image file
        
        Args:
            image_path: Path to image file
            lang: Language for OCR (default: 'eng')
            
        Returns:
            Extracted text
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=lang)
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")
    
    def extract_from_pdf(self, pdf_path: str, use_ocr: bool = True) -> str:
        """
        Extract text from a PDF file
        
        Args:
            pdf_path: Path to PDF file
            use_ocr: If True, use OCR for scanned PDFs
            
        Returns:
            Extracted text
        """
        text = ""
        
        try:
            # First, try to extract text directly (for digital PDFs)
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            # If no text extracted and OCR is enabled, use OCR
            if not text.strip() and use_ocr:
                text = self._ocr_pdf(pdf_path)
            
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def _ocr_pdf(self, pdf_path: str, dpi: int = 300) -> str:
        """
        Use OCR to extract text from scanned PDF
        
        Args:
            pdf_path: Path to PDF file
            dpi: DPI for image conversion
            
        Returns:
            Extracted text
        """
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=dpi)
            
            text = ""
            for i, image in enumerate(images):
                # Extract text from each page
                page_text = pytesseract.image_to_string(image)
                text += f"--- Page {i+1} ---\n{page_text}\n"
            
            return text
        except Exception as e:
            raise Exception(f"Error performing OCR on PDF: {str(e)}")
    
    def extract_from_bytes(self, file_bytes: bytes, file_type: str) -> str:
        """
        Extract text from file bytes (useful for web uploads)
        
        Args:
            file_bytes: File content as bytes
            file_type: 'pdf' or 'image'
            
        Returns:
            Extracted text
        """
        if file_type == 'image':
            try:
                image = Image.open(io.BytesIO(file_bytes))
                text = pytesseract.image_to_string(image)
                return text
            except Exception as e:
                raise Exception(f"Error extracting text from image bytes: {str(e)}")
        
        elif file_type == 'pdf':
            try:
                # Try direct text extraction first
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                text = ""
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                # If no text, would need to save temporarily for OCR
                # (pdf2image requires file path)
                if not text.strip():
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(file_bytes)
                        tmp_path = tmp_file.name
                    
                    try:
                        text = self._ocr_pdf(tmp_path)
                    finally:
                        os.unlink(tmp_path)
                
                return text
            except Exception as e:
                raise Exception(f"Error extracting text from PDF bytes: {str(e)}")
        
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def batch_extract(self, file_paths: List[str]) -> dict:
        """
        Extract text from multiple files
        
        Args:
            file_paths: List of file paths
            
        Returns:
            Dictionary mapping file paths to extracted text
        """
        results = {}
        
        for file_path in file_paths:
            try:
                ext = os.path.splitext(file_path)[1].lower()
                
                if ext == '.pdf':
                    text = self.extract_from_pdf(file_path)
                elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
                    text = self.extract_from_image(file_path)
                else:
                    text = f"Unsupported file format: {ext}"
                
                results[file_path] = text
            except Exception as e:
                results[file_path] = f"Error: {str(e)}"
        
        return results


# Convenience functions
def extract_from_pdf(pdf_path: str, tesseract_path: Optional[str] = None) -> str:
    """Extract text from a PDF file"""
    extractor = OCRExtractor(tesseract_path)
    return extractor.extract_from_pdf(pdf_path)


def extract_from_image(image_path: str, tesseract_path: Optional[str] = None) -> str:
    """Extract text from an image file"""
    extractor = OCRExtractor(tesseract_path)
    return extractor.extract_from_image(image_path)


if __name__ == "__main__":
    # Test the module
    print("OCR Extractor Module")
    print("=" * 50)
    print("\nUsage:")
    print("  from ocr_extractor import extract_from_pdf, extract_from_image")
    print("  text = extract_from_pdf('statement.pdf')")
    print("  text = extract_from_image('statement.jpg')")
