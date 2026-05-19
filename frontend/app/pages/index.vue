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
import '~/assets/css/task.css'

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
