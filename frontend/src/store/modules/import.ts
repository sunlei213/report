import { defineStore } from 'pinia'
import importApi from '@/api/import'
import { ImportState } from '@/types'

export const useImportStore = defineStore('import', {
  state: (): ImportState => ({
    loading: false,
    lastImport: null
  }),
  actions: {
    async importDaily(file: File) {
      this.loading = true
      try {
        const res = await importApi.importDaily(file)
        this.lastImport = res
        return res
      } finally {
        this.loading = false
      }
    },
    async importFixed(file: File) {
      this.loading = true
      try {
        const res = await importApi.importFixed(file)
        this.lastImport = res
        return res
      } finally {
        this.loading = false
      }
    },
    async importPrivate(file: File) {
      this.loading = true
      try {
        const res = await importApi.importPrivate(file)
        this.lastImport = res
        return res
      } finally {
        this.loading = false
      }
    },
    async importRelations(file: File) {
      this.loading = true
      try {
        const res = await importApi.importRelations(file)
        this.lastImport = res
        return res
      } finally {
        this.loading = false
      }
    },
    async importAdjustments(file: File) {
      this.loading = true
      try {
        const res = await importApi.importAdjustments(file)
        this.lastImport = res
        return res
      } finally {
        this.loading = false
      }
    }
  }
})