import { defineStore } from 'pinia'
import managersApi from '@/api/managers'
import { ManagerGroup, Manager, ManagersState } from '@/types'

export const useManagersStore = defineStore('managers', {
  state: (): ManagersState => ({
    groups: [],
    managers: [],
    selectedGroup: null
  }),
  getters: {
    groupById: (state) => (id: number) => {
      return state.groups.find(g => g.id === id)
    },
    managerById: (state) => (id: number) => {
      return state.managers.find(m => m.id === id)
    }
  },
  actions: {
    async fetchGroups() {
      try {
        const res = await managersApi.getGroups()
        this.groups = res.data
        return res.data
      } catch (error) {
        throw error
      }
    },

    async fetchManagers(groupId: number) {
      try {
        const res = await managersApi.getManagers(groupId)
        this.managers = res.data
        return res.data
      } catch (error) {
        throw error
      }
    },

    async saveGroup({ id, data }: { id?: number, data: ManagerGroup }) {
      try {
        await managersApi.saveGroup({ ...data, id })
        await this.fetchGroups()
      } catch (error) {
        throw error
      }
    },

    async deleteGroup(id: number) {
      try {
        await managersApi.deleteGroup(id)
        await this.fetchGroups()
      } catch (error) {
        throw error
      }
    },

    async reorderGroup({ id, newOrder }: { id: number, newOrder: number }) {
      try {
        await managersApi.reorderGroup(id, newOrder)
        await this.fetchGroups()
      } catch (error) {
        throw error
      }
    },

    async saveManager({ groupId, data }: { groupId: number, data: Manager }) {
      try {
        await managersApi.saveManager(groupId, data)
        await this.fetchManagers(groupId)
      } catch (error) {
        throw error
      }
    },

    async updateManager({ groupId, id, data }: { groupId: number, id: number, data: Manager }) {
      try {
        await managersApi.updateManager(id, data)
        await this.fetchManagers(groupId)
      } catch (error) {
        throw error
      }
    },

    async deleteManager({ groupId, id }: { groupId: number, id: number }) {
      try {
        await managersApi.deleteManager(id)
        await this.fetchManagers(groupId)
      } catch (error) {
        throw error
      }
    }
  }
})