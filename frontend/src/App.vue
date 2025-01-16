<template>
  <el-container>
    <el-header>
      <el-menu mode="horizontal" router>
        <el-menu-item index="/report">报表查看</el-menu-item>
        <el-menu-item index="/import">数据导入</el-menu-item>
        <el-menu-item index="/settings">系统设置</el-menu-item>
      </el-menu>
    </el-header>
    
    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

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