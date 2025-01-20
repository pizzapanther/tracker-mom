import Dexie from "dexie";

export const db = new Dexie("tmomdb");
db.version(1).stores({
  active: "follow_pubkey",
  invited: "public",
});

class KeyDB {
  add_active_key(key_obj) {
    return db.active.put(key_obj);
  }

  get_active_key(pubkey) {
    return db.active.get(pubkey);
  }

  add_invite_key(key_obj) {
    return db.invited.put(key_obj);
  }

  delete_invite(pubkey) {
    return db.invited.delete(pubkey);
  }

  async inactive_follows() {
    return db.invited.toArray();
  }

  async clear() {
    await db.delete({ disableAutoOpen: false });
  }
}

export default KeyDB;
