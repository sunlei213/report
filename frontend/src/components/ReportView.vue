<template>
  <div class="report-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>报表查看</span>
          <div class="header-controls">
            <el-date-picker
              v-model="month"
              type="month"
              format="YYYY-MM"
              value-format="YYYYMM"
              placeholder="选择月份"
            />
            <el-button 
              type="primary" 
              @click="handleGenerate"
              :loading="isLoading"
            >
              生成报表
            </el-button>
            <el-button 
              type="success" 
              @click="handleExport"
              :disabled="!hasData"
            >
              导出Excel
            </el-button>
          </div>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="日常数据" name="daily">
          <el-table
            v-loading="isLoading"
            :data="dailyReport.rows"
            border
            style="width: 100%"
            :summary-method="getSummary"
            show-summary
          >
            <!-- 固定列 -->
            <el-table-column 
              prop="客户经理" 
              label="客户经理" 
              fixed="left"
              min-width="120"
            />
            <el-table-column 
              prop="所属组" 
              label="所属组"
              fixed="left"
              min-width="120"
            />
            
            <!-- 动态列 -->
            <template v-for="header in dynamicHeaders" :key="header">
              <el-table-column 
                :prop="header"
                :label="header"
                :align="getColumnAlign(header)"
                :formatter="getColumnFormatter(header)"
                :class-name="getColumnClass(header)"
                min-width="120"
              />
            </template>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="重点数据" name="key">
          <el-table
            v-loading="isLoading"
            :data="keyReport.rows"
            border
            style="width: 100%"
            :summary-method="getSummary"
            show-summary
          >
            <!-- 固定列 -->
            <el-table-column 
              prop="客户经理" 
              label="客户经理" 
              fixed="left"
              min-width="120"
            />
            <el-table-column 
              prop="所属组" 
              label="所属组"
              fixed="left"
              min-width="120"
            />
            
            <!-- 动态列 -->
            <template v-for="header in dynamicHeaders" :key="header">
              <el-table-column 
                :prop="header"
                :label="header"
                :align="getColumnAlign(header)"
                :formatter="getColumnFormatter(header)"
                :class-name="getColumnClass(header)"
                min-width="120"
              />
            </template>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useReportsStore } from '@/store/modules/reports'

const reportsStore = useReportsStore()

const month = ref('')
const activeTab = ref('daily')

const dailyReport = computed(() => reportsStore.dailyReport)
const keyReport = computed(() => reportsStore.keyReport)
const isLoading = computed(() => reportsStore.isLoading)
const hasData = computed(() => reportsStore.hasData)
// 动态表头(除去固定列)
const dynamicHeaders = computed(() => {
  const headers = dailyReport.value.headers || []
  return headers.filter(h => !['客户经理', '所属组'].includes(h))
})

const handleGenerate = async () => {
  if (!month.value) {
    ElMessage.error('请选择月份')
    return
  }

  try {
    await reportsStore.generateReports(month.value)
    ElMessage.success('报表生成成功')
  } catch (error) {
    ElMessage.error('获取报表数据失败')
  }
}

const handleExport = async () => {
  try {
    await reportsStore.exportExcel()
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

  // 列对齐方式
const getColumnAlign = (header) => {
  if (['客户经理', '所属组'].includes(header)) {
    return 'left'
  }
  return 'right'
}

  // 列格式化
const getColumnFormatter = (header) => {
  if (header.includes('金额') || header.includes('调整')) {
    return (row, column, value) => {
      const formatted = value?.toLocaleString('zh-CN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }) || '0.00'
       // 调整为负数时显示红色
      if (header.includes('调整') && value < 0) { 
        return `<span class="negative">${formatted}</span>`
      }
      return formatted
    }
  }
  if (header.includes('完成率')) {
    return (row, column, value) => {
      return value ? `${(value * 100).toFixed(2)}%` : '0.00%'
    }
  }
  if (header.includes('户数')) {
    return (row, column, value) => {
      return value?.toLocaleString('zh-CN') || '0'
    }
  }
  return undefined
}

 // 列样式
const getColumnClass = (header) => { 
  if (header.includes('调整')) {
    return 'adjustment-column'
  }
  return undefined
}

   // 合计行
const getSummary = ({ columns, data }) => {
  const sums = []
  columns.forEach((column, index) => {
    if (index === 0) {
      sums[index] = '合计'
      return
    }
    if (index === 1) {
      sums[index] = ''
      return
    }
    
    const values = data.map(item => Number(item[column.property]) || 0)
    if (column.property.includes('金额') || 
        column.property.includes('调整') || 
        column.property.includes('户数')) {
      sums[index] = values.reduce((prev, curr) => prev + curr, 0)
    } else if (column.property.includes('完成率')) {
        // 完成率合计 = 金额合计 / 目标合计
      const groupName = column.property.split('完成率')[0]
      const amounts = data.map(item => Number(item[`${groupName}金额`]) || 0)
      const totalAmount = amounts.reduce((prev, curr) => prev + curr, 0)
      const targets = data.map(item => {
        const rate = item[column.property] || 0
        const amount = item[`${groupName}金额`] || 0
        return rate > 0 ? amount / rate : 0
      })
      const totalTarget = targets.reduce((prev, curr) => prev + curr, 0)
      sums[index] = totalTarget > 0 ? totalAmount / totalTarget : 0
    } else {
      sums[index] = ''
    }
  })
  return sums
}
</script>

<style scoped>
.report-container {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.header-controls {
  display: flex;
  gap: 10px;
}
.adjustment-column {
  background-color: #f5f7fa;
}
:deep(.negative) {
  color: #f56c6c;
}
</style>