<template>
  <div>
    <tmom-title>Login to Continue</tmom-title>
    <q-form class="q-gutter-md" @submit="onSubmit">
      <q-input outlined v-model="email" label="E-Mail" type="email" required />
      <q-input
        outlined
        v-model="password"
        label="Password"
        type="password"
        required
      />
      <q-btn type="submit" color="primary">Login</q-btn>
    </q-form>
  </div>
</template>
<script>
import { ref } from "vue";
import { useQuasar } from "quasar";
import { useRouter, useRoute } from "vue-router";

import useAppStore from "@/services/store.js";

export default {
  setup() {
    const $q = useQuasar();
    const store = useAppStore();

    var email = ref("");
    var password = ref("");

    const router = useRouter();
    const route = useRoute();

    // async function restore_follows() {
    //   var resp = await api.list_follows();
    //   var follows = resp.data.items;
    //   var db = new KeyDB();
    //   await db.clear();

    //   var updates = [];
    //   follows.forEach((f) => {
    //     var emachine = new EMachine(null, null, f.follow_pubkey);
    //     updates.push({ id: f.id, pubkey: emachine.pubkey });
    //     emachine.store_active_key(f.follow_pubkey);
    //   });

    //   await api.rebuild_keys(updates);
    // }

    function onSubmit() {
      store
        .login(email.value, password.value)
        .then(() => {
          router.push(route.query.next);
        })
        .catch((err) => {
          console.log(err);
          $q.dialog({
            message: "Error with Login.",
            title: "Error",
            color: "negative",
          });
        });
    }
    return { email, password, onSubmit };
  },
};
</script>
