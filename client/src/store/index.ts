import { createStore } from 'vuex'
import exampleModule from './modules/example'

export interface RootState {
  example: ReturnType<typeof exampleModule.state>
}

const store = createStore<RootState>({
  modules: {
    example: exampleModule,
  },
})

export default store
