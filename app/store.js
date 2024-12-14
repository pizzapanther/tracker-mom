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
    report_location(coords) {
      console.log("Reporting:", coords);
      if (api.isAuthenticated()) {
        var messages = [];

        for (var i = 0; i < this.follows.length; i++) {
          var f = this.follows[i];
          messages.push({ following: f.following.id, payload: "narf" });
        }

        api
          .location_push(messages)
          .then(() => {})
          .catch((e) => {
            console.error(e);
          });
      }
    },
  },
});

export default useAppStore;
