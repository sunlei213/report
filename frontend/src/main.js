import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './assets/styles/import.css'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from './utils/axios'

const app = createApp(App)

app.config.globalProperties.$axios = axios

app.use(ElementPlus)
app.use(router)
app.use(store)

app.mount('#app')