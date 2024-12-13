<template>
  <h1>
    <span v-if="$slots.default">
      <slot></slot>
    </span>
    <span class="app">Tracker.mom</span>
  </h1>
</template>
<script>
import { useSlots } from "vue";

export default {
  setup() {
    var slots = useSlots();

    document.title = `${slots.default()[0].children} - Tracker Mom`;
  },
};
</script>
<style @scoped>
h1 {
  display: flex;

  span:first-child {
    flex: 1;
  }

  .app {
    font-size: 80%;
    font-weight: normal;
  }
}
</style>
