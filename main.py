from src.recorder import Recorder
from src.executor import Executor

def main():
    print("选择模式: 1. 录制行为  2. 执行行为")
    choice = input("请输入模式编号: ")
    if choice == "1":
        recorder = Recorder()
        recorder.start_recording()
    elif choice == "2":
        executor = Executor()
        executor.execute_actions()
    else:
        print("无效选择，请重试。")

if __name__ == "__main__":
    main()