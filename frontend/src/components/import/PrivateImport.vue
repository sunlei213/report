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

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

export default {
  name: 'PrivateImport',
  setup() {
    const store = useStore()
    const uploadUrl = '/api/import/private'
    const loading = computed(() => store.state.import.loading)

    const handleSuccess = (response) => {
      if (response.status === 'success') {
        ElMessage.success(response.message)
        store.commit('import/SET_LAST_IMPORT', response)
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
      store.commit('import/SET_LOADING', true)
      return true
    }

    return {
      uploadUrl,
      loading,
      handleSuccess,
      handleError,
      beforeUpload
    }
  }
}
</script> 