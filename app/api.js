import axios from "axios";
import ls from "localstorage-ttl";

class API {
  constructor() {
    this.ax = axios.create({
      baseURL: import.meta.env.VITE_SERVER_URL,
      timeout: 10000,
    });

    this.auth_token = null;
    this.restore_auth();
  }

  restore_auth() {
    var token = ls.get("auth-token");
    if (token) {
      this.auth_token = token;
    }
  }

  set_auth(data) {
    this.auth_token = data.meta.session_token;
  }

  store_auth(data) {
    var now = Date.now();
    var exp = new Date(data.expires).getTime();

    // expire 4 hours before token expires/default django 14 days
    var ttl = exp - now - 60 * 60 * 1000 * 4;
    ls.set("auth-token", this.auth_token, ttl);
  }

  isAuthenticated() {
    const token = ls.get("auth-token");

    if (token) {
      this.auth_token = token;
      return true;
    }

    return false;
  }

  auth_config(kwargs) {
    kwargs = kwargs || {};
    var config = { ...kwargs, headers: { "X-Session-Token": this.auth_token } };
    return config;
  }

  login(email, password) {
    return this.ax.post("/api/auth/app/v1/auth/login", { email, password });
  }

  auth_check() {
    // return this.ax.get('/api/auth/app/v1/auth/session', this.auth_config());
    return this.ax.get("/api/v1/exchange/auth/check", this.auth_config());
  }

  list_follows() {
    return this.ax.get("/api/v1/exchange/follow/list", this.auth_config());
  }

  location_push(messages) {
    return this.ax.post(
      "/api/v1/exchange/location/push",
      messages,
      this.auth_config(),
    );
  }

  pull_messages() {
    return this.ax.get(
      `/api/v1/exchange/location/list?ts=${Date.now()}`,
      this.auth_config(),
    );
  }

  create_invite(pubkey) {
    return this.ax.post(
      "/api/v1/exchange/follow/request",
      { pubkey },
      this.auth_config(),
    );
  }

  get_invite(code) {
    return this.ax.get(
      "/api/v1/exchange/follow/accept",
      this.auth_config({ params: { code } }),
    );
  }

  accept_invite(code, pubkey) {
    return this.ax.post(
      "/api/v1/exchange/follow/accept",
      { code, pubkey },
      this.auth_config(),
    );
  }
}

export default API;
