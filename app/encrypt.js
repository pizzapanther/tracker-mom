import { ECIES_CONFIG, PrivateKey, PublicKey, decrypt, encrypt } from "eciesjs";

ECIES_CONFIG.ellipticCurve = "x25519";
ECIES_CONFIG.symmetricAlgorithm = "xchacha20";

class EMachine {
  constructor(private_key, public_key) {
    this.encoder = new TextEncoder();
    this.decoder = new TextDecoder();

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
}

export default EMachine;
