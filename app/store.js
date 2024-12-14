import { defineStore } from "pinia";

import API from "@/api.js";

var api = new API();

export const useAppStore = defineStore("appstate", {
  state: () => {
    return {
      authenticated: false,
      follows: [],
    };
  },
  getters: {},
  actions: {
    async get_follows() {
      if (api.isAuthenticated()) {
        var resp = await api.list_follows();
        this.follows = resp.data.items;
        return resp.data.items;
      }
    },
  },
});

export default useAppStore;
