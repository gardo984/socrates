import type { Module, ActionContext } from 'vuex'
import type { RootState } from '@/store'
import type { User } from '@/types/user'
import apiClient from '@/api/client'
import router from '@/router'

export interface AuthState {
  currentUser: User | null
  token: string | null
  loading: boolean
  error: string | null
}

type AuthCtx = ActionContext<AuthState, RootState>

function loadFromStorage(): { currentUser: User | null; token: string | null } {
  try {
    const token = localStorage.getItem('auth_token')
    const userRaw = localStorage.getItem('auth_user')
    return {
      token,
      currentUser: userRaw ? (JSON.parse(userRaw) as User) : null,
    }
  } catch {
    return { currentUser: null, token: null }
  }
}

const authModule: Module<AuthState, RootState> = {
  namespaced: true,
  state: (): AuthState => {
    const persisted = loadFromStorage()
    return {
      currentUser: persisted.currentUser,
      token: persisted.token,
      loading: false,
      error: null,
    }
  },
  mutations: {
    SET_CURRENT_USER(state: AuthState, user: User | null) {
      state.currentUser = user
    },
    SET_TOKEN(state: AuthState, token: string | null) {
      state.token = token
    },
    SET_LOADING(state: AuthState, value: boolean) {
      state.loading = value
    },
    SET_ERROR(state: AuthState, value: string | null) {
      state.error = value
    },
    CLEAR_AUTH(state: AuthState) {
      state.currentUser = null
      state.token = null
      state.error = null
    },
    UPDATE_CURRENT_USER(state: AuthState, user: User) {
      state.currentUser = user
      localStorage.setItem('auth_user', JSON.stringify(user))
    },
  },
  actions: {
    async login({ commit }: AuthCtx, credentials: { email: string; password: string }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const loginRes = await apiClient.post<{ access_token: string; token_type: string }>(
          '/auth/login/',
          credentials,
        )
        const token = loginRes.data.access_token
        commit('SET_TOKEN', token)
        localStorage.setItem('auth_token', token)

        const meRes = await apiClient.get<User>('/auth/me')
        const user = meRes.data
        commit('SET_CURRENT_USER', user)
        localStorage.setItem('auth_user', JSON.stringify(user))

        router.push('/')
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Login failed'
        commit('SET_ERROR', msg)
        throw e
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async fetchCurrentUser({ commit, state }: AuthCtx) {
      if (!state.token) return
      try {
        const res = await apiClient.get<User>('/auth/me')
        commit('SET_CURRENT_USER', res.data)
        localStorage.setItem('auth_user', JSON.stringify(res.data))
      } catch {
        commit('CLEAR_AUTH')
        localStorage.removeItem('auth_token')
        localStorage.removeItem('auth_user')
      }
    },
    logout({ commit }: AuthCtx) {
      commit('CLEAR_AUTH')
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_user')
      router.push('/login')
    },
  },
}

export default authModule
