import api from './index'

export default {
  // 数据导入
  importDaily(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/import/daily', formData)
  },
  
  importFixed(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/import/fixed', formData)
  },
  
  importPrivate(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/import/private', formData)
  },
  
  importRelations(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/import/relations', formData)
  },
  
  importAdjustments(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/import/adjustments', formData)
  }
} 