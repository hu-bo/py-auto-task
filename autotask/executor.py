import json
import pyautogui
from autotask.utils import find_image_in_screenshot

class Executor:
    def __init__(self, input_file="recording/actions.json"):
        self.input_file = input_file

    def execute_actions(self):
        print("开始执行行为...")
        with open(self.input_file, "r") as f:
            actions = json.load(f)

        for action in actions.get("actions", []):
            if action["type"] == "click":
                if action["image"]:
                    print(f"尝试通过文字 '{action['text']}' 定位...")
                    # 模拟点击（此处可扩展为基于文字定位）
                    # 截图
                    position = find_image_in_screenshot(action["image"])
                    if position:
                        print(f"找到匹配位置，坐标: {position}")
                        # pyautogui.click(position[0], position[1])
                        pyautogui.click(action["x"], action["y"])
                    else:
                        print("未找到匹配位置")
                        # pyautogui.click(action["x"], action["y"])
                else:
                    print(f"尝试通过坐标 ({action['x']}, {action['y']}) 点击...")
                    pyautogui.click(action["x"], action["y"])
            elif action["type"] == "key_press":
                print(f"尝试按键: {action['key']}")
                if hasattr(action["key"], 'char'):
                    pyautogui.press(action["key"].char)
                else:
                    pyautogui.press(str(action["key"]))
        print("行为执行完成。")