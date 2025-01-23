import { Module } from 'vuex'
import { RootState } from '../index'
import productsApi from '@/api/products'
import { Group, Product, ProductsState } from '@/types'

const productsModule: Module<ProductsState, RootState> = {
  namespaced: true,
  state: () => ({
    groups: [],
    products: [],
    selectedGroup: null
  }),
  mutations: {
    SET_GROUPS(state, groups: Group[]) {
      state.groups = groups
    },
    SET_PRODUCTS(state, products: Product[]) {
      state.products = products
    },
    SET_SELECTED_GROUP(state, groupId: number | null) {
      state.selectedGroup = groupId
    }
  },
  actions: {
    async fetchGroups({ commit }) {
      try {
        const res = await productsApi.getGroups()
        commit('SET_GROUPS', res.data)
        return res.data
      } catch (error) {
        throw error
      }
    },

    async fetchProducts({ commit }, groupId: number) {
      try {
        const res = await productsApi.getProducts(groupId)
        commit('SET_PRODUCTS', res.data)
        return res.data
      } catch (error) {
        throw error
      }
    },

    async saveGroup({ dispatch }, { id, data }: { id?: number, data: Group }) {
      try {
        await productsApi.saveGroup({ ...data, id })
        await dispatch('fetchGroups')
      } catch (error) {
        throw error
      }
    },

    async deleteGroup({ dispatch }, id: number) {
      try {
        await productsApi.deleteGroup(id)
        await dispatch('fetchGroups')
      } catch (error) {
        throw error
      }
    },

    async reorderGroup({ dispatch }, { id, newOrder }: { id: number, newOrder: number }) {
      try {
        await productsApi.reorderGroup(id, newOrder)
        await dispatch('fetchGroups')
      } catch (error) {
        throw error
      }
    },

    async saveProduct({ dispatch }, { groupId, data }: { groupId: number, data: Product }) {
      try {
        await productsApi.saveProduct(groupId, data)
        await dispatch('fetchProducts', groupId)
      } catch (error) {
        throw error
      }
    },

    async updateProduct({ dispatch }, { groupId, id, data }: { groupId: number, id: number, data: Product }) {
      try {
        await productsApi.updateProduct(id, data)
        await dispatch('fetchProducts', groupId)
      } catch (error) {
        throw error
      }
    },

    async deleteProduct({ dispatch }, { groupId, id }: { groupId: number, id: number }) {
      try {
        await productsApi.deleteProduct(id)
        await dispatch('fetchProducts', groupId)
      } catch (error) {
        throw error
      }
    }
  },
  getters: {
    groupById: (state) => (id: number) => {
      return state.groups.find(g => g.id === id)
    },
    productById: (state) => (id: number) => {
      return state.products.find(p => p.id === id)
    }
  }
}

export default productsModule