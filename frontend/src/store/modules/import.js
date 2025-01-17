import importApi from '@/api/import'

const state = {
  loading: false,
  lastImport: null
}

const mutations = {
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_LAST_IMPORT(state, data) {
    state.lastImport = data
  }
}

const actions = {
  async importDaily({ commit }, file) {
    commit('SET_LOADING', true)
    try {
      const res = await importApi.importDaily(file)
      commit('SET_LAST_IMPORT', res)
      return res
    } finally {
      commit('SET_LOADING', false)
    }
  },
  async importFixed({ commit }, file) {
    commit('SET_LOADING', true)
    try {
      const res = await importApi.importFixed(file)
      commit('SET_LAST_IMPORT', res)
      return res
    } finally {
      commit('SET_LOADING', false)
    }
  },
  async importPrivate({ commit }, file) {
    commit('SET_LOADING', true)
    try {
      const res = await importApi.importPrivate(file)
      commit('SET_LAST_IMPORT', res)
      return res
    } finally {
      commit('SET_LOADING', false)
    }
  },
  async importRelations({ commit }, file) {
    commit('SET_LOADING', true)
    try {
      const res = await importApi.importRelations(file)
      commit('SET_LAST_IMPORT', res)
      return res
    } finally {
      commit('SET_LOADING', false)
    }
  },
  async importAdjustments({ commit }, file) {
    commit('SET_LOADING', true)
    try {
      const res = await importApi.importAdjustments(file)
      commit('SET_LAST_IMPORT', res)
      return res
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
} 