import api from './index'

export default {
  // 报表
  getDailyReport(month) {
    return api.get(`/report/daily/${month}`)
  },
  
  getKeyReport(month) {
    return api.get(`/report/key/${month}`)
  },
  
  exportExcel(month) {
    return api.get(`/report/export/${month}`, {
      responseType: 'blob'
    })
  }
} 