import { defineStore } from 'pinia'
import productsApi from '@/api/products'
import { Group, Product, ProductsState } from '@/types'

export const useProductsStore = defineStore('products', {
  state: (): ProductsState => ({
    groups: [],
    products: [],
    selectedGroup: null
  }),
  getters: {
    groupById: (state) => (id: number) => {
      return state.groups.find(g => g.id === id)
    },
    productById: (state) => (id: number) => {
      return state.products.find(p => p.id === id)
    }
  },
  actions: {
    async fetchGroups() {
      try {
        const res = await productsApi.getGroups()
        this.groups = res.data
        return res.data
      } catch (error) {
        throw error
      }
    },

    async fetchProducts(groupId: number) {
      try {
        const res = await productsApi.getProducts(groupId)
        this.products = res.data
        return res.data
      } catch (error) {
        throw error
      }
    },

    async saveGroup({ id, data }: { id?: number, data: Group }) {
      try {
        await productsApi.saveGroup({ ...data, id })
        await this.fetchGroups()
      } catch (error) {
        throw error
      }
    },

    async deleteGroup(id: number) {
      try {
        await productsApi.deleteGroup(id)
        await this.fetchGroups()
      } catch (error) {
        throw error
      }
    },

    async reorderGroup({ id, newOrder }: { id: number, newOrder: number }) {
      try {
        await productsApi.reorderGroup(id, newOrder)
        await this.fetchGroups()
      } catch (error) {
        throw error
      }
    },

    async saveProduct({ groupId, data }: { groupId: number, data: Product }) {
      try {
        await productsApi.saveProduct(groupId, data)
        await this.fetchProducts(groupId)
      } catch (error) {
        throw error
      }
    },

    async updateProduct({ groupId, id, data }: { groupId: number, id: number, data: Product }) {
      try {
        await productsApi.updateProduct(id, data)
        await this.fetchProducts(groupId)
      } catch (error) {
        throw error
      }
    },

    async deleteProduct({ groupId, id }: { groupId: number, id: number }) {
      try {
        await productsApi.deleteProduct(id)
        await this.fetchProducts(groupId)
      } catch (error) {
        throw error
      }
    }
  }
})