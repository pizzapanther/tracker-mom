<template>
  <q-layout view="hHh lpR fFf">
    <q-page-container class="main-container">
      <RouterView />
    </q-page-container>

    <q-footer elevated class="text-white">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="/img/tmom-192.png" />
          </q-avatar>
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>
<script>
import start_bg_watcher from "@/bg-location.js";

export default {
  setup() {
    if (Capacitor.getPlatform() != "web") {
      start_bg_watcher();
    }
  },
};
</script>
<style>
h1 {
  margin: 0;
  font-weight: bold;
  font-size: 1.3rem;
  line-height: 1.3rem;
  padding: 0 5px 10px 5px;
}

.main-container {
  padding: 10px 5px;
}
</style>
