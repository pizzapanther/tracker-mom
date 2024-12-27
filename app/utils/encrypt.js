import { Buffer } from "buffer";
import { ECIES_CONFIG, PrivateKey, PublicKey, decrypt, encrypt } from "eciesjs";

import KeyDB from "@/utils/db.js";

globalThis.Buffer = Buffer;
ECIES_CONFIG.ellipticCurve = "x25519";
ECIES_CONFIG.symmetricAlgorithm = "xchacha20";

var db = new KeyDB();

class EMachine {
  constructor(private_key, public_key, follow_pubkey) {
    this.encoder = new TextEncoder();
    this.decoder = new TextDecoder();

    if (private_key && public_key) {
      this.private_key = PrivateKey.fromHex(private_key);
      this.public_key = PublicKey.fromHex(public_key);
    } else {
      this.private_key = new PrivateKey();
      this.public_key = this.private_key.publicKey;
    }

    if (follow_pubkey) {
      this.follow_pubkey = PublicKey.fromHex(follow_pubkey);
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
    db.add_active_key(obj);
  }

  store_invited_key() {
    var obj = {
      private: this.private_key.toHex(),
      public: this.public_key.toHex(),
      created: Date.now(),
    };
    db.add_invite_key(obj);
  }

  static emachine_for(pubkey, data) {
    return new Promise((resolve, reject) => {
      db.get_active_key(pubkey)
        .then((obj) => {
          var emachine = new EMachine(
            obj.private,
            obj.public,
            obj.follow_pubkey,
          );
          resolve(emachine);
        })
        .catch((e) => {
          reject(e);
        });
    });
  }

  encrypt(data) {
    data = Buffer.from(JSON.stringify(data));
    return encrypt(this.follow_pubkey.toBytes(), data).toString("base64");
  }

  decrypt(data) {
    data = Buffer.from(data, "base64");
    data = decrypt(this.private_key.secret, data);
    return Buffer.from(data).toString();
  }
}

export default EMachine;
