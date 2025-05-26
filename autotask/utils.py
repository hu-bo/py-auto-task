import os
import cv2
import pyautogui
import numpy as np
# import matplotlib.pyplot as plt
import uuid

def capture_and_crop(x, y, width=80, height=60):
    # Step 1: Capture screenshot
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    # Step 2: Crop the initial region
    x1, y1 = max(0, int(x - width // 2)), max(0, int(y - height // 2))
    x2, y2 = int(x + width // 2), int(y + height // 2)
    cropped = screenshot[y1:y2, x1:x2]

    # Step 3: Convert to grayscale and preprocess
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    # Step 4: Check if the image is pure white or pure black
    if np.all(gray == 255):  # Pure white
        print("Detected pure white image, skipping further cropping.")
        return cropped
    if np.all(gray == 0):  # Pure black
        print("Detected pure black image, skipping further cropping.")
        return cropped
    # Step 5: Threshold the image
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # # Step 6: Find contours
    # contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # # Step 7: Calculate the bounding box of all contours
    # if contours:
    #     # Merge all contours into a single bounding box
    #     x, y, w, h = cv2.boundingRect(np.vstack(contours))

    #     # Ensure the cropping region is within bounds
    #     height, width = cropped.shape[:2]
    #     x1, y1 = max(0, x), max(0, y)
    #     x2, y2 = min(width, x + w), min(height, y + h)

    #     # Step 8: Crop to the bounding box
    #     cropped = cropped[y1:y2, x1:x2]

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
    在全屏截图中查找裁切的小图位置
    :param template_path: 小图的文件路径
    :return: 小图在全屏图中的位置 (x, y)，如果未找到则返回 None
    """
    # 截取全屏图像
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)  # 转换为 OpenCV 格式
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    template_path = os.path.normpath(template_path)

    # 加载小图模板
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        raise FileNotFoundError(f"模板文件 {template_path} 未找到")
    if len(template.shape) == 3 and template.shape[2] == 3:  # 如果模板是彩色图像
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)  # 转换为灰度

    # 模板匹配
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    # plt.imshow(result, cmap='hot')
    # plt.colorbar()
    # plt.show()
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(f"最大相似度: {max_val}")
    # 设置相似度阈值
    threshold = 0.7  # 相似度阈值，0.8 表示 80% 相似
    if max_val >= threshold:
        print(f"找到匹配位置，相似度: {max_val}")
        template_height, template_width = template.shape[:2]
        center_x = max_loc[0] + template_width // 2
        center_y = max_loc[1] + template_height // 2
        return (center_x, center_y)  # 返回小图左上角的坐标 (x, y)
    else:
        print("未找到匹配位置")
        return None