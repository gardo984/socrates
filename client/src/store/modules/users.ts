import type { Module, ActionContext } from 'vuex'
import type { RootState } from '@/store'
import type { User, UserCreate, UserUpdate } from '@/types/user'
import apiClient from '@/api/client'

export interface UsersState {
  users: User[]
  loading: boolean
  error: string | null
}

type UserCtx = ActionContext<UsersState, RootState>

const usersModule: Module<UsersState, RootState> = {
  namespaced: true,
  state: (): UsersState => ({
    users: [],
    loading: false,
    error: null,
  }),
  mutations: {
    SET_LOADING(state: UsersState, value: boolean) {
      state.loading = value
    },
    SET_ERROR(state: UsersState, value: string | null) {
      state.error = value
    },
    SET_USERS(state: UsersState, users: User[]) {
      state.users = users
    },
    ADD_USER(state: UsersState, user: User) {
      state.users.push(user)
    },
    UPDATE_USER(state: UsersState, updated: User) {
      const idx = state.users.findIndex((u) => u.id === updated.id)
      if (idx !== -1) state.users[idx] = updated
    },
    REMOVE_USER(state: UsersState, userId: number) {
      state.users = state.users.filter((u) => u.id !== userId)
    },
  },
  actions: {
    async fetchUsers({ commit }: UserCtx) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const res = await apiClient.get<User[]>('/users/')
        commit('SET_USERS', res.data)
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Failed to fetch users'
        commit('SET_ERROR', msg)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async createUser({ commit }: UserCtx, data: UserCreate) {
      commit('SET_ERROR', null)
      try {
        const res = await apiClient.post<User>('/users/', data)
        commit('ADD_USER', res.data)
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Failed to create user'
        commit('SET_ERROR', msg)
      }
    },
    async updateUser({ commit }: UserCtx, payload: { id: number; data: UserUpdate }) {
      commit('SET_ERROR', null)
      try {
        const res = await apiClient.put<User>(`/users/${payload.id}`, payload.data)
        commit('UPDATE_USER', res.data)
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Failed to update user'
        commit('SET_ERROR', msg)
      }
    },
    async deleteUser({ commit }: UserCtx, userId: number) {
      commit('SET_ERROR', null)
      try {
        await apiClient.delete(`/users/${userId}`)
        commit('REMOVE_USER', userId)
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Failed to delete user'
        commit('SET_ERROR', msg)
      }
    },
  },
}

export default usersModule
