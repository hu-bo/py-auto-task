import os
from document.addEventListener("keydown", function (event) {
    // 检查是否按下 Ctrl+S 或 Cmd+S
    if ((event.ctrlKey || event.metaKey) && event.key === "s") {
        event.preventDefault(); // 阻止默认行为（如保存页面）
        if (window.pywebview) {
            window.pywebview.api.stop_recording().then(response => {
                console.log(response); // 输出后端返回的消息
                alert("录制已停止");
            });
        }
    }
});.src.recorder import Recorder
from app.src.executor import Executor

class Api:
    def __init__(self):
        self.recorder = Recorder()
        self.executor = Executor()
        self.recording_dir = "recording"  # 任务文件存储目录

    def start_recording(self):
        """启动录制任务"""
        self.recorder.start_recording()
        return "录制任务已启动"
    def stop_recording(self):
            self.recorder.stop()
            return "Recording stopped"
    def execute_task(self, task_name):
        """执行指定任务"""
        task_path = os.path.join(self.recording_dir, task_name)
        if os.path.exists(task_path):
            self.executor.execute_task(task_path)
            return f"任务 {task_name} 已执行"
        return f"任务 {task_name} 不存在"

    def get_tasks(self):
        """获取任务列表"""
        if not os.path.exists(self.recording_dir):
            os.makedirs(self.recording_dir)  # 如果目录不存在则创建
        return [f for f in os.listdir(self.recording_dir) if os.path.isfile(os.path.join(self.recording_dir, f))]