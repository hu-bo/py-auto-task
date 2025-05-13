import json
import pyautogui
from src.utils import find_image_on_screen

class Executor:
    def __init__(self, input_file="recording/actions.json"):
        self.input_file = input_file

    def execute_actions(self):
        print("开始执行行为...")
        with open(self.input_file, "r") as f:
            actions = json.load(f)
        for action in actions:
            if action["type"] == "click":
                if action["text"]:
                    print(f"尝试通过文字 '{action['text']}' 定位...")
                    # 模拟点击（此处可扩展为基于文字定位）
                else:
                    print(f"尝试通过坐标 ({action['x']}, {action['y']}) 点击...")
                    pyautogui.click(action["x"], action["y"])
        print("行为执行完成。")