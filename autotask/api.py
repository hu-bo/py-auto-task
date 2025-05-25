import os
import json
from autotask.executor import Executor
from autotask.recorder import Recorder


class Api:
    def __init__(self):
        self.recorder = Recorder()
        self.recording_dir = "recording"  # 任务文件存储目录

    def start_recording(self):
        """启动录制任务"""
        self.recorder.start_recording()
        return "录制任务已启动"
    def stop_recording(self):
            self.recorder.stop_recording()
            return "Recording stopped"
    def execute_task(self, task_id):

        """执行指定任务"""
        # 读取任务文件
        task_file = os.path.join(self.recording_dir, f"{task_id}")
        print(task_file)
        if not os.path.exists(task_file):
            return "任务文件不存在"

        self.executor = Executor(task_file)
        self.executor.execute_actions()
        return "任务执行完成"

    def get_tasks(self):
        """获取任务列表"""

        if not os.path.exists(self.recording_dir):
            os.makedirs(self.recording_dir)  # 如果目录不存在则创建
        files = []
        for file in os.listdir(self.recording_dir):
            print(file)
            if os.path.isfile(os.path.join(self.recording_dir, file)):
                # 读取文件内容
                with open(os.path.join(self.recording_dir, file), 'r') as f:
                    content = f.read()
                    # 处理文件内容
                    # 这里可以添加对文件内容的解析逻辑
                    # 例如，假设文件内容是 JSON 格式的任务数据
                    task_data = json.loads(content)
                    files.append({
                        "name": file,
                        "id": task_data["id"]
                    })
        return files
