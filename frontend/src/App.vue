<template>
  <el-container>
    <el-header>
      <Header />
    </el-header>
    
    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<script>
import Header from './components/Header.vue'

export default {
  components: {
    Header
  } 
}
</script>

<style>
.el-header {
  padding: 0;
  height: auto !important;
}
.el-main {
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}
</style> 