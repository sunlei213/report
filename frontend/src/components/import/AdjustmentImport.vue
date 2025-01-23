<template>
  <div class="adjustment-import">
    <el-upload
      class="upload-demo"
      :action="uploadUrl"
      :on-success="handleSuccess"
      :on-error="handleError"
      :before-upload="beforeUpload"
      accept=".xlsx,.xls"
    >
      <el-button type="primary">选择调整数据文件</el-button>
      <template #tip>
        <div class="el-upload__tip">
          请上传调整数据Excel文件，包含以下列：日期、账号、产品代码、产品名称、客户经理、金额、原因、备注
        </div>
      </template>
    </el-upload>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useImportStore } from '@/store/modules/import'
import { ElMessage } from 'element-plus'

const importStore = useImportStore()
const uploadUrl = '/api/import/adjustments'

const handleSuccess = (response) => {
  if (response.status === 'success') {
    ElMessage.success(response.message)
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
  return true
}
</script>

<style scoped>
.adjustment-import {
  padding: 20px;
}
</style>