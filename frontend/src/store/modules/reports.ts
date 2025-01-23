import { Module } from 'vuex'
import { RootState } from '../index'
import reportsApi from '@/api/reports'
import { ReportData, ReportsState } from '@/types'


const reportsModule: Module<ReportsState, RootState> = {
  namespaced: true,
  state: () => ({
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
  }),
  mutations: {
    SET_DAILY_REPORT(state, report: ReportData) {
      state.dailyReport = report
    },
    SET_KEY_REPORT(state, report: ReportData) {
      state.keyReport = report
    },
    SET_LOADING(state, loading: boolean) {
      state.loading = loading
    },
    SET_CURRENT_MONTH(state, month: string) {
      state.currentMonth = month
    }
  },
  actions: {
    async generateReports({ commit }, month: string) {
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
  },
  getters: {
    isLoading: state => state.loading,
    hasData: state => state.dailyReport.rows.length > 0 || state.keyReport.rows.length > 0
  }
}

export default reportsModule