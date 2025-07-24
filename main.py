import threading
import webview
from taskmaster.api import Api



def run_webview(api):
    # 启动 WebView 窗口
    window = webview.create_window(
        title="任务管理界面",
        url="http://localhost:5173/",  # 指向 HTML 文件路径
        # url="http://127.0.0.1:4173",  # 指向 HTML 文件路径
        js_api=api
    )
    # 绑定快捷键
    window.events.key_press += api.recorder.on_key_press
    webview.start(debug=True)

def main():
    # 创建 API 实例
    api = Api()
    # api.start_recording()  # 启动录制任务
    run_webview(api)

if __name__ == "__main__":
    main()



