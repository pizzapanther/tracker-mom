<template>
  <q-layout view="hHh lpR fFf">
    <q-page-container class="main-container">
      <RouterView />
    </q-page-container>

    <q-footer elevated class="text-white">
      <q-tabs>
        <q-route-tab
          to="/"
          name="home"
          icon="img:/img/tmom-192.png"
          label="Dashboard"
        />
        <q-route-tab
          to="/follows/"
          name="Follows"
          icon="mdi-account-group"
          label="Follows"
        />
      </q-tabs>
    </q-footer>
  </q-layout>
</template>
<script>
import start_bg_watcher from "@/bg-location.js";
import useAppStore from "@/store.js";

export default {
  setup() {
    start_bg_watcher();

    const store = useAppStore();
    store.$subscribe((mutation, state) => {
      console.log("Auth", state.authenticated);
    });
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
