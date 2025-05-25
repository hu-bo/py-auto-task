import threading
import webview
from autotask.api import Api



def run_webview(api):
    # 启动 WebView 窗口
    webview.create_window(
        title="任务管理界面",
        url="http://localhost:5173/",  # 指向 HTML 文件路径
        js_api=api
    )
    webview.start()

def main():
    # 创建 API 实例
    api = Api()

    run_webview(api)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("应用程序被用户中断。正在退出...")

if __name__ == "__main__":
    main()



