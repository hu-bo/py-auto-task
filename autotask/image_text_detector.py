import cv2
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageTextDetector:
    def __init__(self, image, lang="eng+chi_sim", preprocess=True):
        """
        Initialize the ImageTextDetector with an image.

        Parameters:
            image (numpy.ndarray): Input image.
            lang (str): Language(s) for OCR (default: "eng+chi_sim").
            preprocess (bool): Whether to preprocess the image before OCR (default: True).
        """
        self.lang = lang
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
            str: Detected text from the image.
        """
        # Perform OCR on the entire image
        text = pytesseract.image_to_string(self.image, lang=self.lang)
        return text

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
            self.ocr_data = pytesseract.image_to_data(self.image, lang=self.lang, output_type=pytesseract.Output.DICT)

        # Iterate through detected text
        for i, text in enumerate(self.ocr_data["text"]):
            if target_text.lower() in text.lower():  # Case-insensitive match
                x, y, w, h = self.ocr_data["left"][i], self.ocr_data["top"][i], self.ocr_data["width"][i], self.ocr_data["height"][i]
                return (x, y)  # Return top-left corner of the text

        return None  # Return None if text is not found