/**
 * 认证状态管理模块
 * 使用Pinia管理用户认证状态
 * 包含登录、登出功能
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import router from '@/router'
import { tr } from 'element-plus/es/locale'


export const useAuthStore = defineStore('auth', () => {
  const token = ref('')
  const username = ref('')

  const isAuthenticated = ref(false)

  function setUser(name: string) { // 设置用户名
    username.value = name
  }

  function setToken(tokenValue: string) { // 设置 Token
    token.value = tokenValue
    localStorage.setItem('token', tokenValue)
    isAuthenticated.value = true
  }

  function checkAuth() { // 检查 Token
    const tokenValue = localStorage.getItem('token')
    if (tokenValue) {
      token.value = tokenValue
      isAuthenticated.value = true
    } else {
      isAuthenticated.value = false
    }
    return isAuthenticated.value
  }

  function logout() {
    token.value = ''
    username.value = ''
    isAuthenticated.value = false
    localStorage.removeItem('token'); // 清除 Token
    router.push('/login')
  }

  return {
    token,
    username,
    isAuthenticated,
    setUser,
    setToken,
    checkAuth,
    logout
  }
})