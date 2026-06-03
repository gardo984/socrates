<template>
  <div class="page">
    <h1>Home</h1>
    <p>Welcome to the Socrates project. This is the home page.</p>
    <div class="card">
      <h3>Counter Example</h3>
      <p>Count: {{ count }}</p>
      <div class="actions">
        <button class="btn" @click="increment">Increment</button>
        <button class="btn btn-secondary" @click="reset">Reset</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const count = computed(() => store.state.example.count)

function increment() {
  store.dispatch('example/increment')
}

function reset() {
  store.dispatch('example/reset')
}
</script>

<style scoped>
.page {
  max-width: 720px;
}

h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

p {
  color: #64748b;
  line-height: 1.6;
}

.card {
  margin-top: 24px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 24px;
}

.card h3 {
  margin: 0 0 12px;
  font-size: 1.1rem;
  color: #1e293b;
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

.btn {
  padding: 8px 20px;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  background-color: #3b82f6;
  color: #ffffff;
  transition: background-color 0.15s;
}

.btn:hover {
  background-color: #2563eb;
}

.btn-secondary {
  background-color: #e2e8f0;
  color: #475569;
}

.btn-secondary:hover {
  background-color: #cbd5e1;
}
</style>
