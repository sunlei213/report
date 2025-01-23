import api, { ApiResponse } from './index'
import { ManagerGroup, Manager } from '@/types'


export default {
  // 客户经理组
  getGroups(): Promise<ApiResponse<ManagerGroup[]>> {
    return api.get('/settings/manager-groups')
  },
  
  saveGroup(data: ManagerGroup): Promise<ApiResponse<ManagerGroup>> {
    return data.id ? 
      api.put(`/settings/manager-groups/${data.id}`, data) :
      api.post('/settings/manager-groups', data)
  },
  
  deleteGroup(id: number): Promise<ApiResponse<void>> {
    return api.delete(`/settings/manager-groups/${id}`)
  },
  
  reorderGroup(id: number, newOrder: number): Promise<ApiResponse<void>> {
    return api.put('/settings/manager-groups/reorder', { id, newOrder })
  },
  
  // 客户经理
  getManagers(groupId: number): Promise<ApiResponse<Manager[]>> {
    return api.get(`/settings/manager-groups/${groupId}/managers`)
  },
  
  saveManager(groupId: number, data: Manager): Promise<ApiResponse<Manager>> {
    return api.post(`/settings/manager-groups/${groupId}/managers`, data)
  },
  
  updateManager(id: number, data: Manager): Promise<ApiResponse<Manager>> {
    return api.put(`/settings/managers/${id}`, data)
  },
  
  deleteManager(id: number): Promise<ApiResponse<void>> {
    return api.delete(`/settings/managers/${id}`)
  },
  
  reorderManager(id: number, newOrder: number): Promise<ApiResponse<void>> {
    return api.put('/settings/managers/reorder', { id, newOrder })
  }
}