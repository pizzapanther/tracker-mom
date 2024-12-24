import { openDB } from "idb";

function fail(e) {
  throw e;
}

class KeyDB {
  constructor() {
    openDB("tmomdb", 1, { upgrade: (db) => this.upgrade(db) })
      .then((db) => {
        this.db = db;
      })
      .catch(fail);
    this.active_store = "active_keys";
    this.invite_store = "invited_keys";
  }

  upgrade(db) {
    console.log("NARF");
    if (!db.objectStoreNames.contains(this.active_store)) {
      db.createObjectStore(this.active_store, { keyPath: "follow_pubkey" });
    }

    if (!db.objectStoreNames.contains(this.invite_store)) {
      db.createObjectStore(this.invite_store, { keyPath: "public" });
    }
  }

  add_active_key(key_obj) {
    this.db
      .add(this.active_store, key_obj)
      .then(() => {})
      .catch(fail);
  }

  get_active_key(pubkey) {
    return this.db.get(this.active_store, pubkey);
  }

  add_invite_key(key_obj) {
    this.db
      .add(this.invite_store, key_obj)
      .then(() => {})
      .catch(fail);
  }
}

export default KeyDB;
