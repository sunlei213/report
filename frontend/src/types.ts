/**
 * 类型定义文件
 * 包含应用程序中使用的主要数据类型
 */
// 导入状态
export interface ImportState {
    loading: boolean
    lastImport: any | null
  }

// 产品组
export interface Group {
    id: number
    name: string
    order: number
  }

// 产品
export interface Product {
    id: number
    name: string
    groupId: number
  }

// 产品列表状态
export interface ProductsState {
    groups: Group[]
    products: Product[]
    selectedGroup: number | null
  }
// 管理组
export interface ManagerGroup {
    id?: number
    name: string
    order: number
  }

// 管理人员
export interface Manager {
    id?: number
    name: string
    groupId: number
  }

// 管理人员列表状态
export interface ManagersState {
    groups: ManagerGroup[]
    managers: Manager[]
    selectedGroup: number | null
  }

  // 报表数据
export interface ReportData {
    headers: string[]
    rows: any[]
  }
  
// 报表状态
export interface ReportsState {
    dailyReport: ReportData
    keyReport: ReportData
    loading: boolean
    currentMonth: string
  }