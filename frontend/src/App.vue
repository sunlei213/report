<template>
  <el-container>
    <el-header>
      <Header></Header>
    </el-header> 
    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import Header from '@/components/Header.vue'

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.el-header {
  padding: 0;
  height: auto !important;
}
.el-main {
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}
</style> 