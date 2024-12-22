import { createApp } from "vue";
import { Quasar, Notify, Dialog } from "quasar";
import { createPinia } from "pinia";

import iconSet from "quasar/icon-set/mdi-v7.js";
import "@quasar/extras/roboto-font/roboto-font.css";
import "@quasar/extras/mdi-v7/mdi-v7.css";

import "quasar/dist/quasar.css";

import TmomTitle from "@/components/title.vue";
import ErrorBanner from "@/components/error.vue";

import router from "@/router.js";
import App from "@/app.vue";

const myApp = createApp(App);
const pinia = createPinia();

myApp.use(pinia);
myApp.use(router);
myApp.use(Quasar, {
  plugins: { Notify, Dialog },
  iconSet: iconSet,
  config: {
    brand: {
      primary: "#247d97",
      secondary: "#f2b934",
      accent: "#f24e34",

      dark: "#1d1d1d",
      "dark-page": "#121212",

      positive: "#46b05f",
      negative: "#bd2436",
      info: "#68afc3",
      warning: "#ffce5b",
    },
  },
});

myApp.component("TmomTitle", TmomTitle);
myApp.component("ErrorBanner", ErrorBanner);
myApp.mount("#q-app");
