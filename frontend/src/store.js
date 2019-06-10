import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const types = {
  UPDATE_USERINFO: 'UPDATE_USERINFO'
}

export default new Vuex.Store({
  state: {
    userInfo: {
      name: 'SuperWong'
    }
  },
  mutations: {
    [types.UPDATE_USERINFO]: (state, userinfo) => {
      state.userInfo = userinfo
    }
  },
  actions: {
    updateUserInfo: async ({ commit }, userinfo) => {
      return commit(types.UPDATE_USERINFO, userinfo)
    }
  },
  getters: {
    getUserInfo (state) {
      return state.userInfo
    }
  }
})
