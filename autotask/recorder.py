import json
import uuid
import sys
from concurrent.futures import ThreadPoolExecutor
from pynput import mouse, keyboard
from autotask.utils import capture_and_crop, upload_image
from autotask.image_text_detector import ImageTextDetector

class Recorder:
    def __init__(self, output_file="recording/actions.json"):
        self.output_file = output_file
        self.actions = []
        self.status = "stopped"
        self.executor = ThreadPoolExecutor(max_workers=4) 

    def on_click(self, x, y, button, pressed):
        if pressed:
            screenshot = capture_and_crop(x, y)
            action = {
                "id": str(uuid.uuid4()),  # 生成唯一 ID
                "type": "click",
                "x": x,
                "y": y,
                "text": "",
                "image": ""
            }
              # 异步执行任务
            self.executor.submit(self.process_action, action, screenshot)
            self.actions.append(action)
            print(f"记录行为: {action}")

    def process_action(self, action, screenshot):
        try:
            text_detector = ImageTextDetector(screenshot)
            # 执行耗时任务
            text = text_detector.detect_text()
            image_url = upload_image(text_detector.image)

            # 更新 action 的 text 和 image
            action["text"] = text
            action["image"] = image_url
            print(f"更新行为: {action}")
        except Exception as e:
            print(f"处理行为时发生错误: {e}")
    def on_key_press(self, key):
        print(self.status)
        if self.status == "recording":
            if key == keyboard.Key.f4:
                self.stop_recording()
                print("F4 键被按下，停止录制...")
                return False
            action = {
                "type": "key_press",
                "key": key.char if hasattr(key, 'char') else str(key)
            }
            self.actions.append(action)
            print(f"记录键盘行为: {action}")
        elif self.status == "stopped":
            if key == keyboard.Key.f4:
                sys.exit(0)
                return False

    def start_recording(self):
        print("开始录制行为，按 F4 停止...")
        self.status = "recording"
        # 清空之前的行为
        self.actions = []
        try:
            # 初始化鼠标监听器
            self.mouse_listener = mouse.Listener(on_click=self.on_click)
            self.mouse_listener.start()

            # 初始化键盘监听器
            self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
            self.keyboard_listener.start()
        except KeyboardInterrupt:
            print("录制结束，保存行为...")
            sys.exit(0)
            self.stop_recording()

    def stop_recording(self):
        """停止录制"""

        self.status = "stopped"
        try:
            if self.mouse_listener and self.mouse_listener.is_alive():
                self.mouse_listener.stop()
            if self.keyboard_listener and self.keyboard_listener.is_alive():
                self.keyboard_listener.stop()
            print("录制已手动停止，保存行为...")
            self.save_actions()  # 保存录制的行为
        except Exception as e:
            print(f"停止录制时发生错误: {e}")
            exit(1)


    def save_actions(self):
        """保存录制的行为到文件"""
        with open(self.output_file, "w") as f:
            record = {
                "id": str(uuid.uuid4()), 
                "actions": self.actions,
                "description": "录制的行为"
            }
            json.dump(record, f, indent=4)
        print(f"行为已保存到 {self.output_file}")