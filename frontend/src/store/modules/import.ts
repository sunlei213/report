import { Module } from 'vuex'
import { RootState } from '../index'
import importApi from '@/api/import'
import { ImportState } from '@/types'

const importModule: Module<ImportState, RootState> = {
  namespaced: true,
  state: () => ({
    loading: false,
    lastImport: null
  }),
  mutations: {
    SET_LOADING(state, loading: boolean) {
      state.loading = loading
    },
    SET_LAST_IMPORT(state, data: any) {
      state.lastImport = data
    }
  },
  actions: {
    async importDaily({ commit }, file: File) {
      commit('SET_LOADING', true)
      try {
        const res = await importApi.importDaily(file)
        commit('SET_LAST_IMPORT', res)
        return res
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async importFixed({ commit }, file: File) {
      commit('SET_LOADING', true)
      try {
        const res = await importApi.importFixed(file)
        commit('SET_LAST_IMPORT', res)
        return res
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async importPrivate({ commit }, file: File) {
      commit('SET_LOADING', true)
      try {
        const res = await importApi.importPrivate(file)
        commit('SET_LAST_IMPORT', res)
        return res
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async importRelations({ commit }, file: File) {
      commit('SET_LOADING', true)
      try {
        const res = await importApi.importRelations(file)
        commit('SET_LAST_IMPORT', res)
        return res
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async importAdjustments({ commit }, file: File) {
      commit('SET_LOADING', true)
      try {
        const res = await importApi.importAdjustments(file)
        commit('SET_LAST_IMPORT', res)
        return res
      } finally {
        commit('SET_LOADING', false)
      }
    }
  }
}

export default importModule