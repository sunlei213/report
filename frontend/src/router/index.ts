import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Login from '@/components/Login.vue'
import ReportView from '@/components/ReportView.vue'
import Settings from '@/components/Settings.vue'
import ImportData from '@/components/ImportData.vue'

declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    requiresAuth?: boolean
  }
}

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/reports'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/reports',
    name: 'Reports',
    component: ReportView,
    meta: { title: '报表查看' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { title: '系统设置' }
  },
  {
    path: '/import',
    name: 'Import',
    component: ImportData,
    meta: { title: '数据导入', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || '业绩管理系统'
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (localStorage.getItem('token')) {
      next()
    } else {
      next('/login')
    }
  } else {
    next()
  }
})

export default router