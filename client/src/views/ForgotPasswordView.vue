<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h1 class="auth-brand">Socrates</h1>
        <p class="auth-subtitle">Reset your password</p>
      </div>
      <p class="auth-description">
        Enter your email address and we will send you a link to reset your password.
      </p>
      <form class="auth-form" @submit.prevent="handleReset">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            class="form-input"
            placeholder="you@example.com"
            required
            autocomplete="email"
          />
        </div>
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? 'Sending...' : 'Send Reset Link' }}
        </button>
      </form>
      <div class="auth-footer">
        <router-link to="/login" class="auth-link">Back to Login</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Swal from 'sweetalert2'

const email = ref('')
const loading = ref(false)

async function handleReset() {
  loading.value = true
  // Simulate a brief network request
  await new Promise((resolve) => setTimeout(resolve, 600))
  loading.value = false

  await Swal.fire({
    icon: 'success',
    title: 'Email sent',
    text: 'Check your inbox for the reset link.',
    confirmButtonColor: '#3b82f6',
  })
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f1f5f9;
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 4px 16px rgba(0, 0, 0, 0.04);
  padding: 40px 32px;
}

.auth-header {
  text-align: center;
  margin-bottom: 16px;
}

.auth-brand {
  font-size: 1.75rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
  letter-spacing: -0.02em;
}

.auth-subtitle {
  font-size: 0.9rem;
  color: #64748b;
  margin: 8px 0 0 0;
}

.auth-description {
  font-size: 0.85rem;
  color: #64748b;
  text-align: center;
  margin: 0 0 24px 0;
  line-height: 1.5;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 500;
  color: #475569;
}

.form-input {
  padding: 10px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #1e293b;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.form-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input::placeholder {
  color: #94a3b8;
}

.btn-submit {
  padding: 11px 20px;
  background-color: #3b82f6;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.15s;
  margin-top: 4px;
}

.btn-submit:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-footer {
  text-align: center;
  margin-top: 24px;
}

.auth-link {
  font-size: 0.85rem;
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

.auth-link:hover {
  text-decoration: underline;
}
</style>
