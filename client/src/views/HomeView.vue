<template>
  <main>
    <head>
      <title>任务管理</title>
    </head>

    <!-- 操作区域 -->
    <div id="operation-area">
      <button @click="startRecording">录制任务</button>
    </div>

    <!-- 表格区域 -->
    <div id="task-table">
      <table width="100%">
        <thead>
          <tr>
            <th>任务id</th>
            <th>任务名称</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in tasks" :key="task.id">
            <td>{{ task.id }}</td>
            <td>{{ task.name }}</td>
            <td>
              <button @click="runTask(task.name)">开始</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue";
// import { notification } from "~/components/Notification/index";

// 定义响应式变量
const tasks = ref([]);

onMounted(() => {
  // 页面加载完成后获取任务列表
  setTimeout(() => {
    console.log(window.pywebview)
    getTaskList();
  }, 1000);
});
// 获取任务列表
const getTaskList = async () => {
  const taskList = await window.pywebview.api.get_tasks();
  tasks.value = taskList;
};

// 执行任务
const runTask = async (taskId) => {
  const response = await window.pywebview.api.execute_task(taskId);
  console.log(response);
};

// 开始录制任务
const startRecording = async () => {
  const response = await window.pywebview.api.start_recording();
  // notification.success({
  //   message: "Success",
  //   description: response,
  //   duration: 5,
  // });
};
</script>

<style scoped>
/* 添加样式 */
</style>