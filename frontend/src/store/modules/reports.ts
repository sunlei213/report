import { defineStore } from 'pinia'
import reportsApi from '@/api/reports'
import { ReportData, ReportsState } from '@/types'

export const useReportsStore = defineStore('reports', {
  state: (): ReportsState => ({
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
  getters: {
    isLoading: state => state.loading,
    hasData: state => state.dailyReport.rows.length > 0 || state.keyReport.rows.length > 0
  },
  actions: {
    async generateReports(month: string) {
      this.loading = true
      try {
        const [dailyRes, keyRes] = await Promise.all([
          reportsApi.getDailyReport(month),
          reportsApi.getKeyReport(month)
        ])

        if (dailyRes.status === 'success') {
          this.dailyReport = dailyRes.data
        }
        if (keyRes.status === 'success') {
          this.keyReport = keyRes.data
        }
        this.currentMonth = month
      } catch (error) {
        throw error
      } finally {
        this.loading = false
      }
    },

    async exportExcel() {
      if (!this.currentMonth) {
        throw new Error('请先选择月份')
      }
      return reportsApi.exportExcel(this.currentMonth)
    }
  }
})