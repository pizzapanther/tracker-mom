<template>
  <tmom-title>Invite a Follower</tmom-title>
  <br />
  <q-btn color="primary" @click="new_invite"> Create a New Invite </q-btn>
</template>
<script>
import API from "@/api.js";
import EMachine from "@/encrypt.js";

export default {
  setup() {
    var api = new API();

    function new_invite() {
      var emachine = new EMachine();

      api
        .create_invite(emachine.pubkey)
        .then((resp) => {
          console.log(resp.data);
        })
        .catch((e) => {
          console.error(e);
        });
    }

    return { new_invite };
  },
};
</script>
