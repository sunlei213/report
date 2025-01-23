import api, { ApiResponse } from './index'
import { ReportData } from '@/types'


export default {
  // 报表
  getDailyReport(month: string): Promise<ApiResponse<ReportData>> {
    return api.get(`/report/daily/${month}`)
  },
  
  getKeyReport(month: string): Promise<ApiResponse<ReportData>> {
    return api.get(`/report/key/${month}`)
  },
  
  exportExcel(month: string): Promise<Blob> {
    return api.get(`/report/export/${month}`, {
      responseType: 'blob'
    })
  }
}