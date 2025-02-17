<template>
  <tmom-title>Follows</tmom-title>
  <q-inner-loading :showing="loading" label="Loading..." />
  <q-page padding>
    <q-btn-group flat class="q-mb-md" spread>
      <q-btn
        color="accent"
        size="sm"
        label="Refresh"
        icon="mdi-refresh"
        @click="refresh_follows"
      />
      <q-btn
        color="accent"
        size="sm"
        label="Add"
        icon="mdi-plus"
        to="/follow/add/"
      />
    </q-btn-group>
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
import { mapState } from "pinia";

import useAppStore from "@/services/store.js";

export default {
  setup() {
    const store = useAppStore();
    var loading = ref(false);
    var error = ref("");

    function refresh_follows() {
      loading.value = true;
      error.value = "";

      store
        .get_follows()
        .then((data) => {})
        .catch((e) => {
          console.error(e);
          error.value = "Error loading Follows from server";
        })
        .finally(() => {
          loading.value = false;
        });
    }

    refresh_follows();

    return { loading, error, refresh_follows };
  },
  computed: {
    ...mapState(useAppStore, ["follows"]),
  },
};
</script>
