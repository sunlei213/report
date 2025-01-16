<template>
  <div class="settings-container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="客户经理组设置" name="managers">
        <manager-groups />
      </el-tab-pane>
      <el-tab-pane label="产品组设置" name="products">
        <product-groups />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import ManagerGroups from './settings/ManagerGroups.vue'
import ProductGroups from './settings/ProductGroups.vue'

export default {
  name: 'Settings',
  components: {
    ManagerGroups,
    ProductGroups
  },
  data() {
    return {
      activeTab: 'managers'
    }
  }
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
}
</style> 