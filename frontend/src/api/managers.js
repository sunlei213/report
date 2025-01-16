import api from './index'

export default {
  // 客户经理组
  getGroups() {
    return api.get('/settings/manager-groups')
  },
  
  saveGroup(data) {
    return data.id ? 
      api.put(`/settings/manager-groups/${data.id}`, data) :
      api.post('/settings/manager-groups', data)
  },
  
  deleteGroup(id) {
    return api.delete(`/settings/manager-groups/${id}`)
  },
  
  reorderGroup(id, newOrder) {
    return api.put('/settings/manager-groups/reorder', { id, newOrder })
  },
  
  // 客户经理
  getManagers(groupId) {
    return api.get(`/settings/manager-groups/${groupId}/managers`)
  },
  
  saveManager(groupId, data) {
    return api.post(`/settings/manager-groups/${groupId}/managers`, data)
  },
  
  updateManager(id, data) {
    return api.put(`/settings/managers/${id}`, data)
  },
  
  deleteManager(id) {
    return api.delete(`/settings/managers/${id}`)
  },
  
  reorderManager(id, newOrder) {
    return api.put('/settings/managers/reorder', { id, newOrder })
  }
} 