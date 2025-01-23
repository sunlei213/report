<template>
  <el-menu
      mode="horizontal"
      :default-active="activeIndex"
      background-color="#409EFF"
      :ellipsis="false"
      text-color="#fff"
      active-text-color="#ffd04b"
      router
    >
      <el-menu-item index="/reports">报表</el-menu-item>
      <el-menu-item index="/import">数据导入</el-menu-item>
      <el-menu-item index="/settings">设置</el-menu-item>
      <el-menu-item index="/login" v-if="!authStore.checkAuth()">登录</el-menu-item>
      <el-menu-item index="/" @click="logout()"  v-if="authStore.checkAuth()">退出登录</el-menu-item>
    </el-menu>
</template>

<script setup lang="ts">
  import { useAuthStore } from '@/store/modules/auth'
  import { ref, computed } from 'vue'
  import { useRouter } from 'vue-router'

  const router = useRouter()
  const authStore = useAuthStore()
  
  const activeIndex = computed(() => router.currentRoute.value.path)

  const logout = () => {
    console.log('logout')
    authStore.logout()
  }

</script>

<style scoped>
.el-menu--horizontal > .el-menu-item:nth-child(3) {
  margin-right: auto;
}
</style>