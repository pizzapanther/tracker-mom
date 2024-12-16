<template>
  <q-card class="text-negative" flat v-if="error">
    <q-card-section>
      <h3>{{ error }}</h3>
    </q-card-section>
  </q-card>
</template>
<script>
export default {
  props: ["error"],
  setup() {},
};
</script>
