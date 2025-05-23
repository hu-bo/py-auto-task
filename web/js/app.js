// 调用后端 API 开始录制任务
async function startRecording() {
  const response = await window.pywebview.api.start_recording();
  alert(response);
  loadTasks(); // 重新加载任务列表
}

// 调用后端 API 执行任务
async function executeTask(taskName) {
  const response = await window.pywebview.api.execute_task(taskName);
  alert(response);
}

// 从后端加载任务列表
async function loadTasks() {
  const tasks = await window.pywebview.api.get_tasks();
  const taskList = document.getElementById("task-list");
  taskList.innerHTML = ""; // 清空表格内容

  tasks.forEach(task => {
      const row = document.createElement("tr");

      // 任务名称列
      const nameCell = document.createElement("td");
      nameCell.innerText = task;
      row.appendChild(nameCell);

      // 操作按钮列
      const actionCell = document.createElement("td");
      const executeButton = document.createElement("button");
      executeButton.innerText = "执行";
      executeButton.onclick = () => executeTask(task);
      actionCell.appendChild(executeButton);
      row.appendChild(actionCell);

      taskList.appendChild(row);
  });
}

// 页面加载时初始化任务列表
window.onload = loadTasks;


document.addEventListener("keydown", function (event) {
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
});