<template>
  <div class="wrapper">
    <div class="card">

      <!-- Header -->
      <div class="header">
        <span class="header-icon">✅</span>
        <h1 class="title">Task Manager</h1>
        <p class="subtitle">Stay organized, get things done</p>
      </div>

      <!-- Stats bar -->
      <div class="stats" v-if="tasks.length > 0">
        <span class="badge badge-total">📋 {{ tasks.length }} Total</span>
        <span class="badge badge-done">✔ {{ tasks.filter(t => t.completed).length }} Done</span>
        <span class="badge badge-pending">⏳ {{ tasks.filter(t => !t.completed).length }} Pending</span>
      </div>

      <!-- Input -->
      <div class="input-row">
        <input
          v-model="newTask"
          class="input"
          placeholder="What do you need to do?"
          @keyup.enter="addTask"
        />
        <button class="btn btn-add" @click="addTask">+ Add</button>
      </div>

      <!-- Empty state -->
      <div v-if="tasks.length === 0" class="empty">
        <p>🎉 No tasks yet!</p>
        <small>Add your first task above to get started.</small>
      </div>

      <!-- Task list -->
      <ul v-else class="task-list">
        <li
          v-for="(task, index) in tasks"
          :key="index"
          class="task-item"
          :class="{ completed: task.completed }"
        >
          <div class="task-left">
            <span class="task-status-dot" :class="{ done: task.completed }"></span>
            <span class="task-text">{{ task.title }}</span>
          </div>
          <div class="task-actions">
            <button
              class="btn btn-complete"
              @click="completeTask(index)"
              :disabled="task.completed"
            >
              {{ task.completed ? '✔ Done' : '✔ Complete' }}
            </button>
            <button class="btn btn-delete" @click="deleteTask(index)">🗑 Delete</button>
          </div>
        </li>
      </ul>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const BASE = 'http://127.0.0.1:8000'
const newTask = ref('')
const tasks = ref([])

async function fetchTasks() {
  const res = await fetch(`${BASE}/tasks`)
  tasks.value = await res.json()
}

async function addTask() {
  const title = newTask.value.trim()
  if (!title) return
  await fetch(`${BASE}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title })
  })
  newTask.value = ''
  await fetchTasks()
}

async function completeTask(index) {
  await fetch(`${BASE}/tasks/${index}`, { method: 'PUT' })
  await fetchTasks()
}

async function deleteTask(index) {
  await fetch(`${BASE}/tasks/${index}`, { method: 'DELETE' })
  await fetchTasks()
}

onMounted(fetchTasks)
</script>

<style>
/* Global reset — removes white border around page */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Segoe UI', sans-serif;
}
</style>

<style scoped>
.wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 24px;
}

.card {
  background: #ffffff;
  border-radius: 20px;
  padding: 40px 36px;
  width: 100%;
  max-width: 560px;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.4);
}

/* Header */
.header {
  text-align: center;
  margin-bottom: 28px;
}

.header-icon {
  font-size: 2.4rem;
  display: block;
  margin-bottom: 8px;
}

.title {
  font-size: 2rem;
  font-weight: 800;
  color: #1a1a2e;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 0.88rem;
  color: #888;
  margin-top: 4px;
}

/* Stats */
.stats {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.badge {
  padding: 5px 14px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.badge-total  { background: #e8eaf6; color: #3949ab; }
.badge-done   { background: #e8f5e9; color: #2e7d32; }
.badge-pending { background: #fff8e1; color: #f57f17; }

/* Input */
.input-row {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
}

.input {
  flex: 1;
  padding: 13px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  color: #1a1a2e;
}

.input:focus {
  border-color: #0f3460;
  box-shadow: 0 0 0 3px rgba(15, 52, 96, 0.1);
}

/* Buttons */
.btn {
  padding: 11px 18px;
  border: none;
  border-radius: 12px;
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.1s, opacity 0.2s;
  white-space: nowrap;
}

.btn:active { transform: scale(0.96); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-add {
  background: linear-gradient(135deg, #0f3460, #533483);
  color: #fff;
}

.btn-complete {
  background: #e8f5e9;
  color: #2e7d32;
}

.btn-delete {
  background: #fdecea;
  color: #c62828;
}

/* Task list */
.task-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-radius: 12px;
  background: #f8f9ff;
  border: 1.5px solid #e8eaf6;
  gap: 12px;
  transition: background 0.2s, border-color 0.2s;
}

.task-item.completed {
  background: #f0fdf4;
  border-color: #c8e6c9;
}

.task-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
}

.task-status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #e0e0e0;
  flex-shrink: 0;
  transition: background 0.2s;
}

.task-status-dot.done {
  background: #4caf50;
}

.task-text {
  font-size: 0.95rem;
  color: #1a1a2e;
  word-break: break-word;
}

.task-item.completed .task-text {
  text-decoration: line-through;
  color: #aaa;
}

.task-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

/* Empty state */
.empty {
  text-align: center;
  padding: 32px 0 16px;
  color: #aaa;
}

.empty p {
  font-size: 1.1rem;
  margin-bottom: 6px;
}

.empty small {
  font-size: 0.85rem;
}

/* Responsive */
@media (max-width: 480px) {
  .card { padding: 28px 18px; }

  .input-row { flex-direction: column; }
  .btn-add { width: 100%; }

  .task-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .task-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
