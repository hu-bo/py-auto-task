import webview
from app.api import Api

def main():
    # 创建 API 实例
    api = Api()

    # 启动 WebView 窗口
    webview.create_window(
        title="任务管理界面",
        url="web/index.html",  # 指向 HTML 文件路径
        js_api=api  # 绑定 API
    )
    webview.start()

if __name__ == "__main__":
    main()