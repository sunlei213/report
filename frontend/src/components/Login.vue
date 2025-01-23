<template>
  <el-container class="login-container">
      <el-card class="login-card">
        <h2 class="login-title">用户登录</h2>
        <el-form
          ref="loginForm"
          :model="form"
          :rules="rules"
          label-width="80px"
          class="login-form"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="form.password" type="password" />
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              :loading="loading"
              @click="onSubmit"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-container>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/utils/auth'
import api from '@/api/index'

const authStore = useAuthStore()
const router = useRouter()
const form = reactive({
  username: '',
  password: ''
})
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}
const loading = ref(false)

const onSubmit = async () => {
  loading.value = true
  try {
    const response = await api.post('/auth/login', {
      username: form.username,
      password: form.password
    })
    authStore.setToken(response.data.token)
    authStore.setUser(form.username)
    router.push('/')
  } catch (error) {
    ElMessage.error('登录失败，请检查用户名或密码')
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.login-card {
  background: white;
  padding: 2rem;
}

.login-title {
  text-align: center;
  margin-bottom: 2rem;
}

.login-form {
  max-width: 300px;
  margin: 0 auto;
}
</style>
