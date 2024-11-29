<template>
  <div>
    <q-form class="q-gutter-md">
      <q-input
        filled
        v-model="name"
        label="Your name *"
        hint="Name and surname"
        lazy-rules
        :rules="[ val => val && val.length > 0 || 'Please type something']"
      />
    </q-form>
  </div>
</template>
<script>
import { ref } from 'vue';

export default {
  setup() {
    var name = ref('');

    return {name};
  }
}
</script>
