<template>
  <div class="reset-password">
    <h1 class="page-title">Reset Password</h1>
    <form class="password-form" @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="current-password">Current Password</label>
        <input
          id="current-password"
          v-model="currentPassword"
          type="password"
          class="form-input"
          placeholder="Enter current password"
          required
        />
      </div>
      <div class="form-group">
        <label for="new-password">New Password</label>
        <input
          id="new-password"
          v-model="newPassword"
          type="password"
          class="form-input"
          placeholder="Enter new password"
          required
        />
      </div>
      <div class="form-group">
        <label for="confirm-password">Confirm New Password</label>
        <input
          id="confirm-password"
          v-model="confirmPassword"
          type="password"
          class="form-input"
          placeholder="Confirm new password"
          required
        />
      </div>
      <p v-if="error" class="form-error">{{ error }}</p>
      <p v-if="success" class="form-success">{{ success }}</p>
      <button type="submit" class="btn-submit" :disabled="loading">
        {{ loading ? 'Updating...' : 'Update Password' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import apiClient from '@/api/client'

const store = useStore()
const currentUser = computed(() => store.state.auth.currentUser)

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

async function handleSubmit() {
  error.value = ''
  success.value = ''

  if (newPassword.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }

  if (newPassword.value.length < 8) {
    error.value = 'New password must be at least 8 characters.'
    return
  }

  loading.value = true
  try {
    await apiClient.put(`/users/${currentUser.value?.id}`, {
      current_password: currentPassword.value,
      new_password: newPassword.value,
    })
    success.value = 'Password updated successfully.'
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (e: unknown) {
    const detail =
      (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
      'Failed to update password.'
    error.value = detail
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.reset-password {
  max-width: 480px;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 24px 0;
}

.password-form {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
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
  padding: 10px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #1e293b;
  outline: none;
  transition: border-color 0.15s;
}

.form-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-error {
  font-size: 0.85rem;
  color: #ef4444;
  margin: 0;
}

.form-success {
  font-size: 0.85rem;
  color: #22c55e;
  margin: 0;
}

.btn-submit {
  padding: 10px 20px;
  background-color: #3b82f6;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s;
  align-self: flex-start;
}

.btn-submit:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
