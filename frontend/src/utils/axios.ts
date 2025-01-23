import axios from 'axios'
import { useAuthStore } from './auth'

const instance = axios.create({
  //baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器
instance.interceptors.response.use(
  function (response) {
     // 对响应数据做点什么

    return response },
  function (error){
    if (error.response?.status === 401) {
      // 处理未授权错误
      const authStore = useAuthStore()
      authStore.logout()
    }
    console.error(error)
    return Promise.reject(error)
  }
)

export default instance