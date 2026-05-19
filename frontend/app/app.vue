<template>
  <div>
    <h1>Nuxt + FastAPI</h1>
    <p>{{ message }}</p>
  </div>
</template>

<script setup>
const { data } = await useFetch('/api/hello')
const message = computed(() => data.value?.message ?? 'Loading...')
</script>
