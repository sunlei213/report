import { createStore } from 'vuex'
import reports from './modules/reports'
import managers from './modules/managers'
import products from './modules/products'
import importModule from './modules/import'

export interface RootState {
  version: string
}

const store = createStore<RootState>({
  modules: {
    reports,
    managers,
    products,
    import: importModule
  }
})

export default store