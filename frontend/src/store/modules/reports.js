import reportsApi from '@/api/reports'

const state = {
  dailyReport: {
    headers: [],
    rows: []
  },
  keyReport: {
    headers: [],
    rows: []
  },
  loading: false,
  currentMonth: ''
}

const mutations = {
  SET_DAILY_REPORT(state, report) {
    state.dailyReport = report
  },
  SET_KEY_REPORT(state, report) {
    state.keyReport = report
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_CURRENT_MONTH(state, month) {
    state.currentMonth = month
  }
}

const actions = {
  async generateReports({ commit }, month) {
    commit('SET_LOADING', true)
    try {
      const [dailyRes, keyRes] = await Promise.all([
        reportsApi.getDailyReport(month),
        reportsApi.getKeyReport(month)
      ])

      if (dailyRes.status === 'success') {
        commit('SET_DAILY_REPORT', dailyRes.data)
      }
      if (keyRes.status === 'success') {
        commit('SET_KEY_REPORT', keyRes.data)
      }
      commit('SET_CURRENT_MONTH', month)
    } catch (error) {
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async exportExcel({ state }) {
    if (!state.currentMonth) {
      throw new Error('请先选择月份')
    }
    return reportsApi.exportExcel(state.currentMonth)
  }
}

const getters = {
  isLoading: state => state.loading,
  hasData: state => state.dailyReport.rows.length > 0 || state.keyReport.rows.length > 0
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 