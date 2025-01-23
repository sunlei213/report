
/**
 * 应用程序入口文件
 * 负责初始化Vue应用、配置全局依赖和挂载根组件
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './assets/styles/import.css'
import router from './router/index'
import store from './store/index'
// 注册全局依赖

import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
const app = createApp(App)
app.use(createPinia())
app.use(ElementPlus, {
    locale: zhCn,
  })
app.use(router)

app.mount('#app')