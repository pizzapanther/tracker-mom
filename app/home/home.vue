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
        <l-marker :lat-lng="[m[0], m[1]]" v-for="m in markers">
          <l-icon :icon-url="iconUrl(m[2])" :icon-size="[32, 32]" />
          <l-popup>{{ m[3] }}: {{ m[2] }}</l-popup>
        </l-marker>
      </l-map>
    </div>
  </div>
</template>
<script>
import { ref, watch, computed } from "vue";
import { mapState } from "pinia";

import "leaflet/dist/leaflet.css";
import {
  LMap,
  LMarker,
  LTileLayer,
  LIcon,
  LPopup,
} from "@vue-leaflet/vue-leaflet";
import JsGravatar from "js-gravatar";

import useAppStore from "@/store.js";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LIcon,
    LPopup,
  },
  setup() {
    const store = useAppStore();
    const map = ref(null);
    const center = ref([29.88438040455563, -98.2429306131633]);
    const locations = ref([]);

    watch(store.locations, (oldValue, newValue) => {
      console.log("Locations", newValue);
      let new_locations = [];

      for (let id in newValue) {
        new_locations.push(newValue[id]);
      }

      locations.value = new_locations;
    });

    const markers = computed(() => {
      var ret = [];
      if (store.mylocation) {
        center.value = [store.mylocation[0], store.mylocation[1]];
        ret.push([...store.mylocation, "Me"]);
      }

      return ret;
    });

    function iconUrl(email) {
      return JsGravatar({ email, size: 256, defaultImage: "retro" });
    }

    return { zoom: 11, map, center, locations, markers, iconUrl };
  },
};
</script>
