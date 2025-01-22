<template>
  <header>
    <nav>
      <router-link to="/">首页</router-link>
      <router-link to="/report">报表</router-link>
      <router-link to="/settings">设置</router-link>
      <button v-if="$auth.isAuthenticated()" @click="handleLogout" class="logout-btn">登出</button>
    </nav>
  </header>
</template>

<script>
import { logout } from '@/utils/auth.js'

export default {
  methods: {
    handleLogout() {
      logout()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
nav {
  padding: 1rem;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  margin-left: auto;
  padding: 0.5rem 1rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>