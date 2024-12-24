<template>
  <tmom-title>Location Share Invitation</tmom-title>
  <br />
  <div v-if="invite">
    <h3>
      <span>Invitation from {{ invite.owner.name }}</span>
      <span v-if="invite.owner.email != invite.owner.name"
        >: {{ invite.owner.email }}</span
      >
    </h3>
    <br />
    <q-btn color="primary" @click="accept_invite">Accept Invite</q-btn>
  </div>
  <error-banner :error="error"></error-banner>
</template>
<script>
import { ref } from "vue";
import { useQuasar } from "quasar";
import { useRoute, useRouter } from "vue-router";

import EMachine from "@/utils/encrypt.js";

import API from "@/api.js";

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();
    const $q = useQuasar();
    var api = new API();
    var error = ref(null);
    var invite = ref(null);

    api
      .get_invite(route.params.code)
      .then((resp) => {
        invite.value = resp.data;
      })
      .catch((e) => {
        error.value = "Error Getting Invite Code";
        console.error(e);
      });

    function accept_invite() {
      error.value = null;
      var emachine = new EMachine();

      api
        .accept_invite(route.params.code, emachine.pubkey)
        .then((resp) => {
          $q.notify({
            message: "Location Share Created!",
            position: "top",
            type: "positive",
            timeout: 3000,
          });
          emachine.store_active_key(resp.data.follow_pubkey);
          router.push("/");
        })
        .catch((e) => {
          error.value = "Error Accepting Invite";
          console.error(e);
        });
    }

    return { error, invite, accept_invite };
  },
};
</script>
