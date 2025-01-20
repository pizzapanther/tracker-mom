import { defineStore } from "pinia";

import API from "@/api.js";
import KeyDB from "@/utils/db.js";
import EMachine from "@/utils/encrypt.js";

var api = new API();
var db = new KeyDB();

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
      let inactives = await db.inactive_follows();
      for (var i = 0; i < inactives.length; i++) {
        for (var f = 0; f < follows.length; f++) {
          let inactive = inactives[i];
          let active = follows[f];

          if (inactive.public == active.owner_pubkey) {
            var obj = {
              ...inactive,
              follow_pubkey: active.follow_pubkey,
              created: Date.now(),
            };
            db.add_active_key(obj);
            db.delete_invite(inactive.public);
            // todo: notification
            // todo: remove old pubkey
          }
        }
      }
    },
    async report_location(coords) {
      console.log("Reporting:", coords);

      if (api.isAuthenticated()) {
        var messages = [];
        this.mylocation = [coords.latitude, coords.longitude, api.email];

        console.log(messages, this.follows);
        for (var i = 0; i < this.follows.length; i++) {
          let f = this.follows[i];
          if (!f.emachine) {
            f.emachine = await EMachine.emachine_for(f.follow_pubkey);
          }

          if (f.emachine) {
            let data = {
              latitude: coords.latitude,
              longitude: coords.longitude,
            };
            messages.push({
              following: f.following.id,
              payload: f.emachine.encrypt(data),
            });
          }
        }

        if (messages.length) {
          console.log("Push Messages", messages);
          await api.location_push(messages);
        }
      }
    },
    async pull_messages() {
      let resp = await api.pull_messages();
      resp.data.items.forEach(async (item) => {
        for (var i = 0; i < this.follows.length; i++) {
          let f = this.follows[i];
          if (f.following.id == item.posted_by.id) {
            if (!f.emachine) {
              f.emachine = await EMachine.emachine_for(f.follow_pubkey);
            }

            try {
              var l = await f.emachine.decrypt(item.payload);
            } catch (e) {
              console.error(e);
            }

            console.log(l);
            this.locations[item.posted_by.id] = [
              l.latitude,
              l.longitude,
              l.posted_by.email,
            ];
          }
        }
      });
    },
  },
});

export default useAppStore;
