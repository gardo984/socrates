<template>
  <div class="page">
    <div class="page-header">
      <h1>Users</h1>
      <button class="btn" @click="showCreateForm = true">+ Create User</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <!-- Create / Edit Modal -->
    <div v-if="showCreateForm || editingUser" class="modal-overlay" @click.self="closeForm">
      <div class="modal">
        <h2>{{ editingUser ? 'Edit User' : 'Create User' }}</h2>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>Name</label>
            <input v-model="form.name" type="text" required />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="form.email" type="email" required />
          </div>
          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="closeForm">Cancel</button>
            <button type="submit" class="btn">{{ editingUser ? 'Update' : 'Create' }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Users Table -->
    <table v-if="!loading" class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td class="actions-cell">
            <button class="btn btn-sm btn-secondary" @click="startEdit(user)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="handleDelete(user.id)">Delete</button>
          </td>
        </tr>
        <tr v-if="users.length === 0">
          <td colspan="4" class="empty">No users found.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import type { User, UserCreate, UserUpdate } from '@/types/user'

const store = useStore()

const users = computed(() => store.state.users.users)
const loading = computed(() => store.state.users.loading)
const error = computed(() => store.state.users.error)

const showCreateForm = ref(false)
const editingUser = ref<User | null>(null)

const form = reactive<UserCreate>({
  name: '',
  email: '',
})

onMounted(() => {
  store.dispatch('users/fetchUsers')
})

function closeForm() {
  showCreateForm.value = false
  editingUser.value = null
  form.name = ''
  form.email = ''
}

function startEdit(user: User) {
  editingUser.value = user
  form.name = user.name
  form.email = user.email
}

function handleSubmit() {
  if (editingUser.value) {
    const data: UserUpdate = {}
    if (form.name !== editingUser.value.name) data.name = form.name
    if (form.email !== editingUser.value.email) data.email = form.email
    if (Object.keys(data).length > 0) {
      store.dispatch('users/updateUser', { id: editingUser.value.id, data })
    }
  } else {
    store.dispatch('users/createUser', { ...form })
  }
  closeForm()
}

function handleDelete(userId: number) {
  if (confirm('Are you sure you want to delete this user?')) {
    store.dispatch('users/deleteUser', userId)
  }
}
</script>

<style scoped>
.page {
  max-width: 960px;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.page-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}
.loading,
.error {
  padding: 16px;
  border-radius: 6px;
  margin-bottom: 16px;
}
.loading {
  color: #64748b;
}
.error {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}
.table {
  width: 100%;
  border-collapse: collapse;
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}
.table th,
.table td {
  text-align: left;
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
}
.table th {
  background: #f8fafc;
  font-weight: 600;
  color: #475569;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.table td {
  color: #1e293b;
  font-size: 0.9rem;
}
.table tbody tr:hover {
  background: #f8fafc;
}
.empty {
  text-align: center;
  color: #94a3b8;
  padding: 32px !important;
}
.actions-cell {
  display: flex;
  gap: 6px;
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
.btn-danger {
  background-color: #ef4444;
  color: #ffffff;
}
.btn-danger:hover {
  background-color: #dc2626;
}
.btn-sm {
  padding: 4px 12px;
  font-size: 0.8rem;
}
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}
.modal {
  background: #ffffff;
  border-radius: 10px;
  padding: 28px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12);
}
.modal h2 {
  margin: 0 0 20px;
  font-size: 1.2rem;
  color: #1e293b;
}
.form-group {
  margin-bottom: 16px;
}
.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 500;
  color: #475569;
  margin-bottom: 4px;
}
.form-group input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #1e293b;
  box-sizing: border-box;
}
.form-group input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
.modal-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 24px;
}
</style>
