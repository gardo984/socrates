import type { Module, ActionContext } from 'vuex'
import type { RootState } from '@/store'
import type { Document } from '@/types/document'
import apiClient from '@/api/client'

export interface DocumentsState {
  documents: Document[]
  loading: boolean
  error: string | null
}

type DocCtx = ActionContext<DocumentsState, RootState>

const documentsModule: Module<DocumentsState, RootState> = {
  namespaced: true,
  state: (): DocumentsState => ({
    documents: [],
    loading: false,
    error: null,
  }),
  mutations: {
    SET_LOADING(state: DocumentsState, value: boolean) {
      state.loading = value
    },
    SET_ERROR(state: DocumentsState, value: string | null) {
      state.error = value
    },
    SET_DOCUMENTS(state: DocumentsState, docs: Document[]) {
      state.documents = docs
    },
    ADD_DOCUMENT(state: DocumentsState, doc: Document) {
      state.documents.push(doc)
    },
    REMOVE_DOCUMENT(state: DocumentsState, docId: number) {
      state.documents = state.documents.filter((d) => d.id !== docId)
    },
  },
  actions: {
    async fetchDocuments({ commit }: DocCtx) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const res = await apiClient.get<Document[]>('/documents/')
        commit('SET_DOCUMENTS', res.data)
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Failed to fetch documents'
        commit('SET_ERROR', msg)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async uploadDocument({ commit }: DocCtx, file: File) {
      commit('SET_ERROR', null)
      try {
        const formData = new FormData()
        formData.append('file', file)
        const res = await apiClient.post<Document>('/documents/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        commit('ADD_DOCUMENT', res.data)
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Failed to upload document'
        commit('SET_ERROR', msg)
      }
    },
    async deleteDocument({ commit }: DocCtx, docId: number) {
      commit('SET_ERROR', null)
      try {
        await apiClient.delete(`/documents/${docId}`)
        commit('REMOVE_DOCUMENT', docId)
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Failed to delete document'
        commit('SET_ERROR', msg)
      }
    },
  },
}

export default documentsModule
