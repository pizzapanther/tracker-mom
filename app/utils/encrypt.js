import { ECIES_CONFIG, PrivateKey, PublicKey, decrypt, encrypt } from "eciesjs";

import KeyDB from "@/utils/db.js";

ECIES_CONFIG.ellipticCurve = "x25519";
ECIES_CONFIG.symmetricAlgorithm = "xchacha20";

class EMachine {
  constructor(private_key, public_key) {
    this.encoder = new TextEncoder();
    this.decoder = new TextDecoder();
    this.db = new KeyDB();

    if (private_key && public_key) {
      this.private_key = PrivateKey.fromHex(private_key);
      this.public_key = PublicKey.fromHex(public_key);
    } else {
      this.private_key = new PrivateKey();
      this.public_key = this.private_key.publicKey;
    }
  }

  get pubkey() {
    return this.public_key.toHex();
  }

  get privkey() {
    return this.private_key.toHex();
  }

  store_active_key(follow_key) {
    var obj = {
      private: this.private_key.toHex(),
      public: this.public_key.toHex(),
      follow_pubkey: follow_key,
      created: Date.now(),
    };
    this.db.add_active_key(obj);
  }

  store_invited_key() {
    var obj = {
      private: this.private_key.toHex(),
      public: this.public_key.toHex(),
      created: Date.now(),
    };
    this.db.add_invite_key(obj);
  }
}

export default EMachine;
