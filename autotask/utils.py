import os
import cv2
import pyautogui
import numpy as np
import matplotlib.pyplot as plt
import uuid
import io
from PIL import Image

def capture_and_crop(x, y, width=150, height=90):
    # Step 1: Capture screenshot
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Step 2: Crop initial region
    x1, y1 = max(0, x - width // 2), max(0, y - height // 2)
    x2, y2 = x + width // 2, y + height // 2
    cropped = screenshot[y1:y2, x1:x2]

    # Step 3: Convert to grayscale
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    # Step 4: Check for pure white/black (early exit)
    if np.all(gray == 255) or np.all(gray == 0):
        print("Detected pure color image.")
        return cropped

    # Step 5: Contrast enhancement using CLAHE (for low-light/shadowed images)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Step 6: Threshold with Otsu's method
    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Step 7: Morphological operations to connect broken edges
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)  # Close small gaps

    # Step 8: Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 9: Filter contours by area and position
    if contours:
        # Filter out small contours (e.g., noise)
        min_contour_area = 100  # 根据实际Logo大小调整
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

        if valid_contours:
            # Find the largest contour (assuming it's the logo)
            largest_contour = max(valid_contours, key=cv2.contourArea)
            x_box, y_box, w_box, h_box = cv2.boundingRect(largest_contour)

            # Ensure the contour is not near the edge (exclude shadow-like regions)
            padding = 10  # 排除边缘轮廓
            if x_box > padding and y_box > padding and (x_box + w_box) < (cropped.shape[1] - padding) and (y_box + h_box) < (cropped.shape[0] - padding):
                # Step 10: Centered cropping
                crop_width = 150
                crop_height = 90
                x_center = x_box + w_box // 2
                y_center = y_box + h_box // 2
                x1 = max(0, x_center - crop_width // 2)
                y1 = max(0, y_center - crop_height // 2)
                x2 = min(cropped.shape[1], x1 + crop_width)
                y2 = min(cropped.shape[0], y1 + crop_height)
                cropped = cropped[y1:y2, x1:x2]

    return cropped

def upload_image(local_path, storage_type="local", oss_config=None):
    """
    Upload an image to a storage service and return its URL.

    Parameters:
        local_path (str or ndarray): Path to the local image file or an image array.
        storage_type (str): Storage type, e.g., "local" (default) or "oss".
        oss_config (dict): Configuration for OSS (if storage_type is "oss").

    Returns:
        str: URL of the uploaded image.
    """
    if storage_type == "local":
        # Ensure the images directory exists
        images_dir = os.path.join(os.getcwd(), "images")
        os.makedirs(images_dir, exist_ok=True)

        # If local_path is an ndarray, save it as an image file
        if isinstance(local_path, np.ndarray):
            # 随机生成文件名
            file_name = f"{uuid.uuid4()}.png"
            file_path = os.path.join(images_dir, file_name)
            cv2.imwrite(file_path, local_path)  # Save the ndarray as an image
            return f"{os.path.abspath(file_path)}"
        
        # If local_path is a string, treat it as a file path
        elif isinstance(local_path, str):
            return f"{os.path.abspath(os.path.join(images_dir, local_path))}"
        
        else:
            raise TypeError("local_path must be a string or an ndarray")
    
    elif storage_type == "oss":
        raise ValueError(f"Unsupported storage type: {storage_type}")
    
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")
    
def find_image_in_screenshot(template_path):
    """
    在全屏截图中查找裁切的小图位置（带可视化和图像质量降低）
    :param template_path: 小图的文件路径
    :return: 小图在全屏图中的中心位置 (x, y)，如果未找到则返回 None
    """
    # 截图并分离高质量图像（用于可视化）与低质量图像（用于匹配）
    screenshot = pyautogui.screenshot()
    original_screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 生成低质量图像用于匹配
    quality = 50  # 质量参数（0~100，数值越低质量越差）
    temp_bytes = io.BytesIO()
    screenshot.save(temp_bytes, format='JPEG', quality=quality)
    screenshot_low = Image.open(temp_bytes)
    screenshot_low = cv2.cvtColor(np.array(screenshot_low), cv2.COLOR_RGB2BGR)
    screenshot_low = cv2.cvtColor(screenshot_low, cv2.COLOR_BGR2GRAY)  # 转灰度用于匹配

    # 加载模板
    template_path = os.path.normpath(template_path)
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        raise FileNotFoundError(f"模板文件 {template_path} 未找到")
    if len(template.shape) == 3 and template.shape[2] == 3:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 模板匹配
    result = cv2.matchTemplate(screenshot_low, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(f"最大相似度: {max_val}")

    # 设置阈值
    threshold = 0.7
    if max_val >= threshold:
        print(f"找到匹配位置，相似度: {max_val}")
        template_height, template_width = template.shape[:2]
        top_left = max_loc
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

        # 在原始图像上绘制矩形框和相似度标签
        # cv2.rectangle(original_screenshot, top_left, bottom_right, (255, 0, 0), 2)
        # cv2.putText(
        #     original_screenshot,
        #     f"{max_val:.2f}",
        #     (top_left[0], top_left[1] - 10),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     0.6,
        #     (255, 0, 0),
        #     1
        # )

        # 显示热力图
        # plt.imshow(result, cmap='hot')
        # plt.colorbar()
        # plt.title("Similarity Heatmap (Low Quality Image)")
        # plt.show()

        # # 显示带有标注的清晰图像
        # plt.imshow(cv2.cvtColor(original_screenshot, cv2.COLOR_BGR2RGB))
        # plt.title("Matched Image with Bounding Box (Original Quality)")
        # plt.axis('off')
        # plt.show()

        return (top_left[0] + template_width // 2, top_left[1] + template_height // 2)
    else:
        print("未找到匹配位置")
        return None