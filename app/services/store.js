import { defineStore } from "pinia";

import API from "@/services/api.js";

var api = new API();

export const useAppStore = defineStore("appstate", {
  state: () => {
    return {
      authenticated: false,
      follows: [],
      locations: {},
      mylocation: null,
    };
  },
  getters: {},
  actions: {},
});

export default useAppStore;
