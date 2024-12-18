<template>
  <tmom-title>Invite a Follower</tmom-title>
  <br />
  <div v-if="invite">
    <h3>Invite {{ count }} - Send Via:</h3>
    <em>Use this invite only once</em>
    <br />
    <q-btn color="accent" icon="mdi-mail" target="_blank" :href="links.email">
      &nbsp; E-Mail
    </q-btn>
    &nbsp;&nbsp;&nbsp;
    <q-btn color="accent" target="_blank" :href="links.sms" icon="mdi-message">
      &nbsp; Text Message
    </q-btn>
    <br /><br />
    <strong>URL:</strong> &nbsp;
    <span>{{ invite.url }}</span>
    <br /><br />
    <q-btn color="primary" @click="new_invite"> Create Another Invite </q-btn>
  </div>
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
    var count = ref(0);
    var links = ref({});

    function new_invite() {
      var emachine = new EMachine();
      error.value = null;

      api
        .create_invite(emachine.pubkey)
        .then((resp) => {
          invite.value = resp.data;
          count.value += 1;

          let subject = `Follow Me On Tracker.Mom`;
          let intro =
            "Come follow me and share your location on Tracker.mom. Use the link to join.";
          let post =
            "Tracker.Mom is the secure and private location sharing app for family and friends.";
          let tbody = `${intro} ${resp.data.url}`;
          let ebody = `${encodeURIComponent(intro + "<br><br>")}${encodeURIComponent(resp.data.url + "<br><br>")}${encodeURIComponent(post)}`;
          links.value = {
            email: `mailto:?subject=${encodeURIComponent(subject)}&body=${ebody}`,
            sms: `sms:?&body=${encodeURIComponent(tbody)}`,
          };
        })
        .catch((e) => {
          console.error(e);
          error.value = "Error Creating Invite";
        });
    }

    return { new_invite, error, invite, count, links };
  },
};
</script>
