import { defineStore } from "pinia";

import API from "@/services/api.js";

var api = new API();

export const useAppStore = defineStore("appstate", {
  state: () => {
    return {
      follows: [],
      locations: {},
      mylocation: null,
    };
  },
  getters: {},
  actions: {
    isAuthenticated() {
      return api.isAuthenticated();
    },
    async login(email, password) {
      let resp = await api.login(email, password);
      api.set_auth(resp.data);
      resp = await api.auth_check();
      api.store_auth(resp.data);
      // return restore_follows();
    },
  },
});

export default useAppStore;
