<template>
  <div class="user-info">
    <h1 class="page-title">User Information</h1>
    <div v-if="currentUser" class="info-card">
      <div class="info-row">
        <span class="info-label">Name</span>
        <div v-if="editing" class="info-edit-group">
          <input
            v-model="editName"
            type="text"
            class="edit-input"
            @keyup.enter="handleSave"
            @keyup.escape="handleCancel"
            ref="nameInput"
          />
          <button class="btn btn-sm btn-primary" @click="handleSave" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save' }}
          </button>
          <button class="btn btn-sm btn-secondary" @click="handleCancel">Cancel</button>
        </div>
        <div v-else class="info-value-group">
          <span class="info-value">{{ currentUser.name }}</span>
          <button class="btn-icon" @click="startEditing" title="Edit name">
            <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>
          </button>
        </div>
      </div>
      <div class="info-row">
        <span class="info-label">Email</span>
        <span class="info-value">{{ currentUser.email }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">User ID</span>
        <span class="info-value">#{{ currentUser.id }}</span>
      </div>
    </div>
    <div v-else class="empty-state">
      <p>No user information available.</p>
    </div>
    <p v-if="saveError" class="save-error">{{ saveError }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, nextTick } from 'vue'
import { useStore } from 'vuex'
import apiClient from '@/api/client'
import type { User } from '@/types/user'

const store = useStore()
const currentUser = computed(() => store.state.auth.currentUser)

const editing = ref(false)
const editName = ref('')
const saving = ref(false)
const saveError = ref('')
const nameInput = ref<HTMLInputElement | null>(null)

function startEditing() {
  editName.value = currentUser.value?.name ?? ''
  editing.value = true
  saveError.value = ''
  nextTick(() => nameInput.value?.focus())
}

async function handleSave() {
  if (!currentUser.value || !editName.value.trim()) return
  if (editName.value.trim() === currentUser.value.name) {
    handleCancel()
    return
  }
  saving.value = true
  saveError.value = ''
  try {
    const res = await apiClient.put<User>(`/users/${currentUser.value.id}`, {
      name: editName.value.trim(),
    })
    store.commit('auth/UPDATE_CURRENT_USER', res.data)
    editing.value = false
  } catch {
    saveError.value = 'Failed to update name. Please try again.'
  } finally {
    saving.value = false
  }
}

function handleCancel() {
  editing.value = false
  saveError.value = ''
}
</script>

<style scoped>
.user-info {
  max-width: 600px;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 24px 0;
}

.info-card {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
}

.info-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e293b;
}

.info-value-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-edit-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.edit-input {
  padding: 6px 10px;
  border: 1px solid #3b82f6;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #1e293b;
  outline: none;
  width: 200px;
}

.edit-input:focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.btn {
  padding: 5px 12px;
  border: none;
  border-radius: 5px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.12s;
}

.btn-sm {
  padding: 4px 10px;
  font-size: 0.78rem;
}

.btn-primary {
  background-color: #3b82f6;
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #e2e8f0;
  color: #475569;
}

.btn-secondary:hover {
  background-color: #cbd5e1;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: #94a3b8;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  transition: color 0.12s, background-color 0.12s;
}

.btn-icon:hover {
  color: #3b82f6;
  background-color: #eff6ff;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #94a3b8;
}

.save-error {
  margin-top: 16px;
  padding: 10px 14px;
  background-color: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  border-radius: 6px;
  font-size: 0.85rem;
}
</style>
