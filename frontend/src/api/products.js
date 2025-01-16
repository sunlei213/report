import api from './index'

export default {
  // 产品组
  getGroups() {
    return api.get('/settings/product-groups')
  },
  
  saveGroup(data) {
    return data.id ? 
      api.put(`/settings/product-groups/${data.id}`, data) :
      api.post('/settings/product-groups', data)
  },
  
  deleteGroup(id) {
    return api.delete(`/settings/product-groups/${id}`)
  },
  
  reorderGroup(id, newOrder) {
    return api.put('/settings/product-groups/reorder', { id, newOrder })
  },
  
  // 产品
  getProducts(groupId) {
    return api.get(`/settings/product-groups/${groupId}/products`)
  },
  
  saveProduct(groupId, data) {
    return api.post(`/settings/product-groups/${groupId}/products`, data)
  },
  
  updateProduct(id, data) {
    return api.put(`/settings/products/${id}`, data)
  },
  
  deleteProduct(id) {
    return api.delete(`/settings/products/${id}`)
  }
} 