import json
import cv2
import pytesseract
from pynput import mouse
from src.utils import capture_screenshot, detect_text

class Recorder:
    def __init__(self, output_file="recording/actions.json"):
        self.output_file = output_file
        self.actions = []

    def on_click(self, x, y, button, pressed):
        if pressed:
            screenshot = capture_screenshot()
            text = detect_text(screenshot, x, y)
            action = {
                "type": "click",
                "x": x,
                "y": y,
                "text": text if text else None
            }
            self.actions.append(action)
            print(f"记录行为: {action}")

    def start_recording(self):
        print("开始录制行为，按 Ctrl+C 停止...")
        with mouse.Listener(on_click=self.on_click) as listener:
            try:
                listener.join()
            except KeyboardInterrupt:
                print("录制结束，保存行为...")
                with open(self.output_file, "w") as f:
                    json.dump(self.actions, f, indent=4)
                print(f"行为已保存到 {self.output_file}")