import productsApi from '@/api/products'

const state = {
  groups: [],
  products: [],
  selectedGroup: null
}

const mutations = {
  SET_GROUPS(state, groups) {
    state.groups = groups
  },
  SET_PRODUCTS(state, products) {
    state.products = products
  },
  SET_SELECTED_GROUP(state, group) {
    state.selectedGroup = group
  }
}

const actions = {
  async fetchGroups({ commit }) {
    try {
      const res = await productsApi.getGroups()
      commit('SET_GROUPS', res.data)
      return res.data
    } catch (error) {
      throw error
    }
  },

  async fetchProducts({ commit }, groupId) {
    try {
      const res = await productsApi.getProducts(groupId)
      commit('SET_PRODUCTS', res.data)
      return res.data
    } catch (error) {
      throw error
    }
  },

  async saveGroup({ dispatch }, { id, data }) {
    try {
      await productsApi.saveGroup({ ...data, id })
      await dispatch('fetchGroups')
    } catch (error) {
      throw error
    }
  },

  async deleteGroup({ dispatch }, id) {
    try {
      await productsApi.deleteGroup(id)
      await dispatch('fetchGroups')
    } catch (error) {
      throw error
    }
  },

  async reorderGroup({ dispatch }, { id, newOrder }) {
    try {
      await productsApi.reorderGroup(id, newOrder)
      await dispatch('fetchGroups')
    } catch (error) {
      throw error
    }
  },

  async saveProduct({ dispatch }, { groupId, data }) {
    try {
      await productsApi.saveProduct(groupId, data)
      await dispatch('fetchProducts', groupId)
    } catch (error) {
      throw error
    }
  },

  async updateProduct({ dispatch }, { groupId, id, data }) {
    try {
      await productsApi.updateProduct(id, data)
      await dispatch('fetchProducts', groupId)
    } catch (error) {
      throw error
    }
  },

  async deleteProduct({ dispatch }, { groupId, id }) {
    try {
      await productsApi.deleteProduct(id)
      await dispatch('fetchProducts', groupId)
    } catch (error) {
      throw error
    }
  }
}

const getters = {
  groupById: (state) => (id) => {
    return state.groups.find(g => g.id === id)
  },
  productById: (state) => (id) => {
    return state.products.find(p => p.id === id)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 