import { defineStore } from "pinia";

import API from "@/api.js";
import KeyDB from "@/utils/db.js";

var api = new API();
var db = new KeyDB();

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
        this.sync_follows(resp.data.items)
          .then(() => {})
          .catch(console.error);
        return resp.data.items;
      }
    },
    async sync_follows(follows) {
      db.inactive_follows((inactive) => {
        for (var j = 0; j < follows.length; j++) {
          var active = follows[j];
          console.log(inactive.public, active.owner_pubkey);
          if (inactive.public == active.owner_pubkey) {
            var obj = {
              ...inactive,
              follow_pubkey: active.follow_pubkey,
              created: Date.now(),
            };
            db.add_active_key(obj);
            db.delete_invite(inactive.public);
            // todo notification
          }
        }
      });
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
