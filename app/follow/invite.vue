<template>
  <tmom-title>Invite a Follower</tmom-title>
  <br />
  <div v-if="invite"></div>
  <q-btn v-else color="primary" @click="new_invite">
    Create a New Invite
  </q-btn>
  <error-banner :error="error"></error-banner>
</template>
<script>
import { ref } from "vue";

import API from "@/api.js";
import EMachine from "@/encrypt.js";

import ErrorBanner from "@/components/error.vue";

export default {
  components: { ErrorBanner },
  setup() {
    var api = new API();
    var invite = ref(null);
    var error = ref(null);

    function new_invite() {
      var emachine = new EMachine();
      error.value = null;

      api
        .create_invite(emachine.pubkey)
        .then((resp) => {
          invite.value = resp.data;
        })
        .catch((e) => {
          console.error(e);
          error.value = "Error Creating Invite";
        });
    }

    return { new_invite, error, invite };
  },
};
</script>
