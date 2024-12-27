import { registerPlugin, Capacitor } from "@capacitor/core";
import useAppStore from "@/store.js";

const platform = Capacitor.getPlatform();
if (platform != "web") {
  var BackgroundGeolocation = registerPlugin("BackgroundGeolocation");
}

function watcher_callback(location, error) {
  if (error) {
    if (error.code === "NOT_AUTHORIZED") {
      if (
        window.confirm(
          "This app needs your location, " +
            "but does not have permission.\n\n" +
            "Open settings now?",
        )
      ) {
        // It can be useful to direct the user to their device's
        // settings when location permissions have been denied. The
        // plugin provides the 'openSettings' method to do exactly
        // this.
        BackgroundGeolocation.openSettings();
      }
    }

    return console.error(error);
  }

  return console.log(location);
}

export function app_bg_watcher(store) {
  var options = {
    backgroundMessage: "Tracker Mom running in the background.",
    backgroundTitle: "Tracker Mom Service",

    requestPermissions: true,

    // If "true", stale locations may be delivered while the device
    // obtains a GPS fix. You are responsible for checking the "time"
    // property. If "false", locations are guaranteed to be up to date.
    // Defaults to "false".
    stale: false,

    // The minimum number of metres between subsequent locations. Defaults
    // to 0.
    distanceFilter: 50,
  };

  BackgroundGeolocation.addWatcher(options, watcher_callback).then(
    (watcher_id) => {
      console.log("Watcher Added:", watcher_id);
    },
  );
}

function web_bg_watcher(store) {
  navigator.geolocation.watchPosition(async (position) => {
    await store.report_location(position.coords);
  });
}

async function pull_locations(store) {
  await store.pull_messages();
  setTimeout(async () => await pull_locations(store), 60 * 1000);
}

export function start_bg_watcher() {
  console.log("Starting BG Watcher:", platform);
  const store = useAppStore();

  if (platform == "web") {
    web_bg_watcher(store);
  } else {
    app_bg_watcher(store);
  }

  setTimeout(async () => await pull_locations(store), 3000);
}

export default start_bg_watcher;
