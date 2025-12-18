"""
OCR module for processing bank statements from images and PDFs
"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
from pdf2image import convert_from_path
import re
from datetime import datetime
from typing import List, Dict, Optional


class BankStatementOCR:
    """Processes bank statements using OCR to extract transaction data"""
    
    def __init__(self):
        self.transactions = []
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert PIL Image to OpenCV format
        img_array = np.array(image)
        
        # Convert to grayscale
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Apply thresholding to get binary image
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        # Convert back to PIL Image
        return Image.fromarray(denoised)
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from image using OCR
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Extracted text as string
        """
        image = Image.open(image_path)
        preprocessed = self.preprocess_image(image)
        text = pytesseract.image_to_string(preprocessed)
        return text
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF by converting to images
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text from all pages
        """
        pages = convert_from_path(pdf_path, 300)  # 300 DPI
        full_text = ""
        
        for page_num, page in enumerate(pages):
            preprocessed = self.preprocess_image(page)
            page_text = pytesseract.image_to_string(preprocessed)
            full_text += f"\n--- Page {page_num + 1} ---\n{page_text}"
        
        return full_text
    
    def parse_transactions(self, text: str) -> List[Dict]:
        """
        Parse transactions from extracted text
        
        Args:
            text: OCR extracted text
            
        Returns:
            List of transaction dictionaries
        """
        transactions = []
        lines = text.split('\n')
        
        # Pattern for transaction lines (flexible to handle various formats)
        # Looking for: date, description, amount
        date_pattern = r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
        amount_pattern = r'[-+]?\$?\s*\d+[,.]?\d*\.?\d*'
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to find date
            date_match = re.search(date_pattern, line)
            if date_match:
                date_str = date_match.group(1)
                
                # Try to extract amount (usually at the end)
                amount_matches = re.findall(amount_pattern, line)
                if amount_matches:
                    # Get the last number as amount
                    amount_str = amount_matches[-1].replace('$', '').replace(',', '').strip()
                    try:
                        amount = float(amount_str)
                        
                        # Extract description (text between date and amount)
                        description = line[date_match.end():].strip()
                        # Remove amount from description
                        for amt in amount_matches:
                            description = description.replace(amt, '').strip()
                        
                        if description:
                            transaction = {
                                'date': self._parse_date(date_str),
                                'description': description,
                                'amount': amount
                            }
                            transactions.append(transaction)
                    except ValueError:
                        continue
        
        return transactions
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse date string to datetime object
        
        Args:
            date_str: Date string in various formats
            
        Returns:
            datetime object or None if parsing fails
        """
        formats = [
            '%m/%d/%Y', '%m-%d-%Y',
            '%d/%m/%Y', '%d-%m-%Y',
            '%m/%d/%y', '%m-%d-%y',
            '%d/%m/%y', '%d-%m-%y',
            '%Y/%m/%d', '%Y-%m-%d'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def process_statement(self, file_path: str) -> List[Dict]:
        """
        Process a bank statement file (image or PDF)
        
        Args:
            file_path: Path to the statement file
            
        Returns:
            List of extracted transactions
        """
        if file_path.lower().endswith('.pdf'):
            text = self.extract_text_from_pdf(file_path)
        else:
            text = self.extract_text_from_image(file_path)
        
        transactions = self.parse_transactions(text)
        self.transactions.extend(transactions)
        
        return transactions
