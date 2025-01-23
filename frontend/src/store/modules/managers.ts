import { Module } from 'vuex'
import { RootState } from '../index'
import managersApi from '@/api/managers'
import { ManagerGroup, Manager, ManagersState } from '@/types'


const managersModule: Module<ManagersState, RootState> = {
  namespaced: true,
  state: () => ({
    groups: [],
    managers: [],
    selectedGroup: null
  }),
  mutations: {
    SET_GROUPS(state, groups: ManagerGroup[]) {
      state.groups = groups
    },
    SET_MANAGERS(state, managers: Manager[]) {
      state.managers = managers
    },
    SET_SELECTED_GROUP(state, groupId: number | null) {
      state.selectedGroup = groupId
    }
  },
  actions: {
    async fetchGroups({ commit }) {
      try {
        const res = await managersApi.getGroups()
        commit('SET_GROUPS', res.data)
        return res.data
      } catch (error) {
        throw error
      }
    },

    async fetchManagers({ commit }, groupId: number) {
      try {
        const res = await managersApi.getManagers(groupId)
        commit('SET_MANAGERS', res.data)
        return res.data
      } catch (error) {
        throw error
      }
    },

    async saveGroup({ dispatch }, { id, data }: { id?: number, data: ManagerGroup }) {
      try {
        await managersApi.saveGroup({ ...data, id })
        await dispatch('fetchGroups')
      } catch (error) {
        throw error
      }
    },

    async deleteGroup({ dispatch }, id: number) {
      try {
        await managersApi.deleteGroup(id)
        await dispatch('fetchGroups')
      } catch (error) {
        throw error
      }
    },

    async reorderGroup({ dispatch }, { id, newOrder }: { id: number, newOrder: number }) {
      try {
        await managersApi.reorderGroup(id, newOrder)
        await dispatch('fetchGroups')
      } catch (error) {
        throw error
      }
    },

    async saveManager({ dispatch }, { groupId, data }: { groupId: number, data: Manager }) {
      try {
        await managersApi.saveManager(groupId, data)
        await dispatch('fetchManagers', groupId)
      } catch (error) {
        throw error
      }
    },

    async updateManager({ dispatch }, { groupId, id, data }: { groupId: number, id: number, data: Manager }) {
      try {
        await managersApi.updateManager(id, data)
        await dispatch('fetchManagers', groupId)
      } catch (error) {
        throw error
      }
    },

    async deleteManager({ dispatch }, { groupId, id }: { groupId: number, id: number }) {
      try {
        await managersApi.deleteManager(id)
        await dispatch('fetchManagers', groupId)
      } catch (error) {
        throw error
      }
    }
  },
  getters: {
    groupById: (state) => (id: number) => {
      return state.groups.find(g => g.id === id)
    },
    managerById: (state) => (id: number) => {
      return state.managers.find(m => m.id === id)
    }
  }
}

export default managersModule