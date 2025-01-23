<template>
  <div class="private-import">
    <el-upload
      class="upload-demo"
      :action="uploadUrl"
      :on-success="handleSuccess"
      :on-error="handleError"
      :before-upload="beforeUpload"
      accept=".xlsx,.xls"
      :loading="loading"
    >
      <el-button type="primary" :loading="loading">选择私募产品文件</el-button>
      <template #tip>
        <div class="el-upload__tip">
          请上传私募产品Excel文件，包含以下列：日期、账号、产品代码、产品名称、客户经理、金额等
        </div>
      </template>
    </el-upload>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useImportStore } from '@/store/modules/import'
import { ElMessage } from 'element-plus'

const importStore = useImportStore()
const uploadUrl = '/api/import/private'
const loading = computed(() => importStore.loading)

const handleSuccess = (response) => {
  if (response.status === 'success') {
    ElMessage.success(response.message)
    importStore.lastImport = response
  } else {
    ElMessage.error(response.message)
  }
}

const handleError = () => {
  ElMessage.error('上传失败')
}

const beforeUpload = (file) => {
  const isExcel = /\.(xlsx|xls)$/.test(file.name.toLowerCase())
  if (!isExcel) {
    ElMessage.error('只能上传Excel文件!')
    return false
  }
  importStore.loading = true
  return true
}
</script>

<style scoped>
.private-import {
  padding: 20px;
}
</style>