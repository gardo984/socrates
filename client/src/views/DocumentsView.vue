<template>
  <div class="page">
    <div class="page-header">
      <h1>Documents</h1>
      <button class="btn" @click="triggerUpload">+ Upload Document</button>
      <input
        ref="fileInput"
        type="file"
        accept=".txt,.pdf,.docx"
        style="display: none"
        @change="handleFileSelected"
      />
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <table v-if="!loading" class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Filename</th>
          <th>Type</th>
          <th>Size</th>
          <th>Uploaded At</th>
          <th>User ID</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="doc in documents" :key="doc.id">
          <td>{{ doc.id }}</td>
          <td>{{ doc.filename }}</td>
          <td>{{ doc.file_type ?? '-' }}</td>
          <td>{{ formatSize(doc.file_size) }}</td>
          <td>{{ formatDate(doc.uploaded_at) }}</td>
          <td>{{ doc.user_id ?? '-' }}</td>
          <td>
            <button class="btn btn-sm btn-danger" @click="handleDelete(doc.id)">Delete</button>
          </td>
        </tr>
        <tr v-if="documents.length === 0">
          <td colspan="7" class="empty">No documents found.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

const documents = computed(() => store.state.documents.documents)
const loading = computed(() => store.state.documents.loading)
const error = computed(() => store.state.documents.error)

const fileInput = ref<HTMLInputElement | null>(null)

onMounted(() => {
  store.dispatch('documents/fetchDocuments')
})

function triggerUpload() {
  fileInput.value?.click()
}

function handleFileSelected(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (file) {
    store.dispatch('documents/uploadDocument', file)
    input.value = ''
  }
}

function handleDelete(docId: number) {
  if (confirm('Are you sure you want to delete this document?')) {
    store.dispatch('documents/deleteDocument', docId)
  }
}

function formatSize(bytes: number | null): string {
  if (bytes === null || bytes === undefined) return '-'
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleString()
}
</script>

<style scoped>
.page {
  max-width: 1100px;
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
.btn-sm {
  padding: 4px 12px;
  font-size: 0.8rem;
}
.btn-danger {
  background-color: #ef4444;
  color: #ffffff;
}
.btn-danger:hover {
  background-color: #dc2626;
}
</style>
