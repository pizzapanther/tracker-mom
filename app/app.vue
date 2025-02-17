<template>
  <q-layout view="hHh lpR fFf">
    <q-page-container
      class="main-container"
      style="margin: 0 auto; max-width: 500px"
    >
      <RouterView />
    </q-page-container>

    <q-footer elevated class="text-white">
      <q-tabs>
        <q-route-tab
          to="/"
          name="home"
          :icon="`img:${tmomImg}`"
          label="Dashboard"
        />
        <q-route-tab
          to="/follow/"
          name="Follows"
          icon="mdi-account-group"
          label="Follows"
        />
      </q-tabs>
    </q-footer>
  </q-layout>
</template>
<script>
import start_bg_watcher from "@/services/bg-location.js";
import useAppStore from "@/services/store.js";

import tmomImg from "@/img/tmom-192.png";

export default {
  setup() {
    start_bg_watcher();

    const store = useAppStore();
    store.$subscribe((mutation, state) => {
      console.log("Auth", state.authenticated);
    });
    // store
    //   .get_follows()
    //   .then((data) => {
    //     console.log("Follows Loaded", data);
    //   })
    //   .catch((e) => {
    //     console.error(e);
    //     console.log("Ignoring On Load Error");
    //   });

    return { tmomImg };
  },
};
</script>
<style>
h1 {
  margin: 0;
  font-weight: bold;
  font-size: 1.4rem;
  line-height: 1.4rem;
  padding: 0 5px 10px 5px;
}

h2 {
  margin: 10px 0;
  font-size: 1.3rem;
  line-height: 1.3rem;
  font-weight: bold;
}

h3 {
  margin: 10px 0;
  font-size: 1.2rem;
  line-height: 1.2rem;
  font-weight: bold;
}

.main-container {
  padding: 10px 5px;
}
</style>
