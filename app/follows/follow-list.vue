<template>
  <tmom-title>Follows</tmom-title>
  <q-inner-loading :showing="loading" label="Loading..." />
  <q-page padding>
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="mdi-refresh" color="accent" @click="refresh_follows" />
    </q-page-sticky>
    <q-card class="text-negative" flat v-if="error">
      <q-card-section>
        <h3>{{ error }}</h3>
      </q-card-section>
    </q-card>
    <q-list bordered separator class="rounded-borders" v-if="!loading">
      <q-item v-if="follows.length == 0">
        <q-item-section>
          <q-item-label lines="1">
            <h3>You are not following anyone yet</h3>
          </q-item-label>
        </q-item-section>
      </q-item>
      <q-item v-for="f in follows">
        <q-item-section top>
          <q-item-label lines="1">
            <span>{{ f.following.name }}</span>
          </q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-page>
</template>
<script>
import { ref } from "vue";

import API from "@/api.js";

export default {
  setup() {
    var loading = ref(false);
    var error = ref("");
    var follows = ref([]);
    var api = new API();

    function refresh_follows() {
      loading.value = true;
      error.value = "";

      api
        .list_follows()
        .then((resp) => {
          follows.value = resp.data.items;
        })
        .catch((e) => {
          console.error(e);
          error.value = "Error loading Follows from server";
        })
        .finally(() => {
          loading.value = false;
        });
    }

    refresh_follows();

    return { loading, error, follows, refresh_follows };
  },
};
</script>
