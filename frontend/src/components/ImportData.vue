<template>
  <div class="import-container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="日常委托" name="daily">
        <daily-import />
      </el-tab-pane>
      <el-tab-pane label="固收产品" name="fixed">
        <fixed-import />
      </el-tab-pane>
      <el-tab-pane label="私募产品" name="private">
        <private-import />
      </el-tab-pane>
      <el-tab-pane label="客户关系" name="relations">
        <relation-import />
      </el-tab-pane>
      <el-tab-pane label="调整数据" name="adjustments">
        <adjustment-import />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { ref } from 'vue'
import DailyImport from './import/DailyImport.vue'
import FixedImport from './import/FixedImport.vue'
import PrivateImport from './import/PrivateImport.vue'
import RelationImport from './import/RelationImport.vue'
import AdjustmentImport from './import/AdjustmentImport.vue'

export default {
  name: 'ImportData',
  components: {
    DailyImport,
    FixedImport,
    PrivateImport,
    RelationImport,
    AdjustmentImport
  },
  setup() {
    const activeTab = ref('daily')
    return { activeTab }
  }
}
</script>

<style scoped>
.import-container {
  padding: 20px;
}
</style> 