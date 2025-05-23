import cv2
import pytesseract
import pyautogui
import numpy as np

def capture_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

def detect_text(image, x, y, radius=50):
    h, w, _ = image.shape
    x, y = int(x), int(y)
    x1, y1 = max(0, x - radius), max(0, y - radius)
    x2, y2 = min(w, x + radius), min(h, y + radius)
    cropped = image[y1:y2, x1:x2]
    text = pytesseract.image_to_string(cropped, lang="eng")
    return text.strip()

def find_image_on_screen(template_path):
    screenshot = capture_screenshot()
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY), template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.8:  # 匹配阈值
        return max_loc
    return None