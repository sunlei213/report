<template>
  <div class="import-container">
    <el-card class="import-card">
      <template #header>
        <div class="card-header">
          <span>数据导入</span>
        </div>
      </template>
      
      <el-form label-width="120px">
        <el-form-item label="数据类型">
          <el-select v-model="importType" placeholder="请选择数据类型">
            <el-option label="日常委托数据" value="daily" />
            <el-option label="固收产品数据" value="fixed" />
            <el-option label="私募产品数据" value="private" />
            <el-option label="客户关系数据" value="relations" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="Excel文件">
          <el-upload
            class="upload-demo"
            :action="uploadUrl"
            :on-success="handleSuccess"
            :on-error="handleError"
            :before-upload="beforeUpload"
            accept=".xlsx,.xls"
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                只能上传xlsx/xls文件
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ImportData',
  data() {
    return {
      importType: '',
      uploadUrl: ''
    }
  },
  watch: {
    importType(val) {
      this.uploadUrl = `/api/import/${val}`
    }
  },
  methods: {
    beforeUpload(file) {
      if (!this.importType) {
        this.$message.error('请先选择数据类型')
        return false
      }
      return true
    },
    handleSuccess(response) {
      if (response.status === 'success') {
        this.$message.success(response.message)
      } else {
        this.$message.error(response.message)
      }
    },
    handleError() {
      this.$message.error('上传失败')
    }
  }
}
</script>

<style scoped>
.import-container {
  padding: 20px;
}
.import-card {
  max-width: 600px;
  margin: 0 auto;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 