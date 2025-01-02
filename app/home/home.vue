<template>
  <div>
    <tmom-title>Dashboard</tmom-title>
    <div style="height: 400px; width: 100%">
      <l-map
        ref="map"
        v-model:zoom="zoom"
        :center="center"
        :use-global-leaflet="false"
      >
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          layer-type="base"
          name="OpenStreetMap"
        ></l-tile-layer>
      </l-map>
    </div>
  </div>
</template>
<script>
import { ref } from "vue";
import { mapState } from "pinia";

import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

import useAppStore from "@/store.js";

export default {
  components: {
    LMap,
    LTileLayer,
  },
  setup() {
    const store = useAppStore();
    const map = ref(null);
    const center = ref([29.88438040455563, -98.2429306131633]);

    // if (this.locations.length) {
    //   console.log('Locations', locations);
    //   //map.fitBounds(poly.getBounds());
    //   return;
    // }

    return { zoom: 11, map, center };
  },
  computed: {
    ...mapState(useAppStore, ["locations"]),
  },
};
</script>
