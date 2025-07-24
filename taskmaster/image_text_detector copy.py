import cv2
import numpy as np
import easyocr

class ImageTextDetector:
    def __init__(self, image, lang_list=["en", "ch_sim"], preprocess=True):
        """
        Initialize the ImageTextDetector with an image.

        Parameters:
            image (numpy.ndarray): Input image.
            lang_list (list): List of languages for OCR (default: ["en", "zh"]).
            preprocess (bool): Whether to preprocess the image before OCR (default: True).
        """
        self.reader = easyocr.Reader(lang_list)
        self.preprocess = preprocess
        self.image = self._preprocess_image(image) if preprocess else image
        self.ocr_data = None  # Cache for OCR data

    def _preprocess_image(self, image):
        """
        Preprocess the image (convert to grayscale and binarize).

        Parameters:
            image (numpy.ndarray): Input image.

        Returns:
            numpy.ndarray: Preprocessed image.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply thresholding to binarize the image
        _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary_image

    def detect_text(self):
        """
        Detect all text in the image.

        Returns:
            list: Detected text from the image.
        """
        # Perform OCR on the entire image
        results = self.reader.readtext(self.image)
        return results

    def find_text_coordinate(self, target_text):
        """
        Find the coordinates of the target text in the image.

        Parameters:
            target_text (str): The text to search for.

        Returns:
            tuple: (x, y) coordinates of the top-left corner of the text, or None if not found.
        """
        # Use cached OCR data if available
        if self.ocr_data is None:
            self.ocr_data = self.reader.readtext(self.image)

        # Iterate through detected text
        for result in self.ocr_data:
            text = result[1]
            if target_text.lower() in text.lower():  # Case-insensitive match
                x, y = result[0][0]  # Top-left corner of the bounding box
                return (int(x), int(y))

        return None  # Return None if text is not found



