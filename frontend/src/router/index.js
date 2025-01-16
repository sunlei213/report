import { createRouter, createWebHistory } from 'vue-router'
import ImportData from '@/components/ImportData.vue'
import ReportView from '@/components/ReportView.vue'
import Settings from '@/components/Settings.vue'

const routes = [
  {
    path: '/',
    redirect: '/report'
  },
  {
    path: '/import',
    name: 'Import',
    component: ImportData,
    meta: { title: '数据导入' }
  },
  {
    path: '/report',
    name: 'Report',
    component: ReportView,
    meta: { title: '报表查看' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { title: '系统设置' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || '业绩管理系统'
  next()
})

export default router 