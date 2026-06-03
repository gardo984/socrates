import type { Module } from 'vuex'
import type { ExampleState } from '@/types'

export interface RootState {
  example: ExampleState
}

const exampleModule: Module<ExampleState, RootState> = {
  namespaced: true,
  state: (): ExampleState => ({
    count: 0,
  }),
  mutations: {
    increment(state: ExampleState) {
      state.count++
    },
    reset(state: ExampleState) {
      state.count = 0
    },
  },
  actions: {
    increment({ commit }) {
      commit('increment')
    },
    reset({ commit }) {
      commit('reset')
    },
  },
  getters: {
    count: (state: ExampleState) => state.count,
  },
}

export default exampleModule
