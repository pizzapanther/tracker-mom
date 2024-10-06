import { createApp } from "vue";
import { Quasar } from "quasar";

import "@quasar/extras/roboto-font/roboto-font.css";
import "@quasar/extras/mdi-v7/mdi-v7.css";

import "quasar/dist/quasar.css";

import App from "./app.vue";

const myApp = createApp(App);

myApp.use(Quasar, {
  plugins: {}, // import Quasar plugins and add here
});

myApp.mount("#q-app");
