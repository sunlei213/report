import api from './index'

export default {
  // 数据导入
  importDaily(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/import/daily', formData)
  },
  
  importFixed(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/import/fixed', formData)
  },
  
  importPrivate(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/import/private', formData)
  },
  
  importRelations(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/import/relations', formData)
  },
  
  importAdjustments(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/import/adjustments', formData)
  }
}