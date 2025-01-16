import { createStore } from 'vuex'
import managers from './modules/managers'
import products from './modules/products'
import reports from './modules/reports'

export default createStore({
  modules: {
    managers,
    products,
    reports
  }
}) 