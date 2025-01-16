import managersApi from '@/api/managers'

const state = {
  groups: [],
  managers: [],
  selectedGroup: null
}

const mutations = {
  SET_GROUPS(state, groups) {
    state.groups = groups
  },
  SET_MANAGERS(state, managers) {
    state.managers = managers
  },
  SET_SELECTED_GROUP(state, group) {
    state.selectedGroup = group
  }
}

const actions = {
  async fetchGroups({ commit }) {
    try {
      const res = await managersApi.getGroups()
      commit('SET_GROUPS', res.data)
      return res.data
    } catch (error) {
      throw error
    }
  },

  async fetchManagers({ commit }, groupId) {
    try {
      const res = await managersApi.getManagers(groupId)
      commit('SET_MANAGERS', res.data)
      return res.data
    } catch (error) {
      throw error
    }
  },

  async saveGroup({ dispatch }, { id, data }) {
    try {
      await managersApi.saveGroup({ ...data, id })
      await dispatch('fetchGroups')
    } catch (error) {
      throw error
    }
  },

  async deleteGroup({ dispatch }, id) {
    try {
      await managersApi.deleteGroup(id)
      await dispatch('fetchGroups')
    } catch (error) {
      throw error
    }
  },

  async reorderGroup({ dispatch }, { id, newOrder }) {
    try {
      await managersApi.reorderGroup(id, newOrder)
      await dispatch('fetchGroups')
    } catch (error) {
      throw error
    }
  },

  async saveManager({ dispatch }, { groupId, data }) {
    try {
      await managersApi.saveManager(groupId, data)
      await dispatch('fetchManagers', groupId)
    } catch (error) {
      throw error
    }
  },

  async updateManager({ dispatch }, { groupId, id, data }) {
    try {
      await managersApi.updateManager(id, data)
      await dispatch('fetchManagers', groupId)
    } catch (error) {
      throw error
    }
  },

  async deleteManager({ dispatch }, { groupId, id }) {
    try {
      await managersApi.deleteManager(id)
      await dispatch('fetchManagers', groupId)
    } catch (error) {
      throw error
    }
  }
}

const getters = {
  groupById: (state) => (id) => {
    return state.groups.find(g => g.id === id)
  },
  managerById: (state) => (id) => {
    return state.managers.find(m => m.id === id)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 