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

  store_auth(data) {
    ls.set("auth-token", data.meta.session_token, 1000 * 60 * 60 * 24);
    this.auth_token = data.meta.session_token;
  }

  auth_config() {
    return { headers: { "X-Session-Token": this.auth_token } };
  }

  login(email, password) {
    return this.ax.post("/api/auth/app/v1/auth/login", { email, password });
  }

  auth_check() {
    return this.ax.get("/api/v1/exchange/auth/check", this.auth_config());
    // return this.ax.get('/api/auth/app/v1/auth/session', this.auth_config());
  }
}

export default API;
