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

import API from "@/api.js";

export default {
  setup() {
    const $q = useQuasar();
    var api = new API();
    var email = ref("");
    var password = ref("");

    const router = useRouter();
    const route = useRoute();

    function onSubmit() {
      api
        .login(email.value, password.value)
        .then((resp) => {
          api.set_auth(resp.data);
          return api.auth_check();
        })
        .then((resp) => {
          api.store_auth(resp.data);
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
