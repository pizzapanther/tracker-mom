<template>
  <q-layout view="hHh lpR fFf">
    <q-page-container class="main-container">
      <login-view></login-view>
    </q-page-container>

    <q-footer elevated class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg" />
          </q-avatar>
          <div>Title</div>
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>
<script>
import start_bg_watcher from "@/bg-location.js";
import LoginView from "@/auth/login.vue";

export default {
  components: { LoginView },
  setup() {
    if (Capacitor.getPlatform() != "web") {
      start_bg_watcher();
    }
  },
};
</script>
<style>
.main-container {
  padding: 10px 5px;
}
</style>
