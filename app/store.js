import { defineStore } from "pinia";

export const useAppStore = defineStore("appstate", {
  state: () => {
    return {
      authenticated: false,
    };
  },
  getters: {},
  actions: {},
});

export default useAppStore;
