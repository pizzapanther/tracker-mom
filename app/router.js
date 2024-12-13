import { createWebHistory, createRouter } from "vue-router";

import API from "@/api.js";
import HomeView from "@/home/home.vue";
import LoginView from "@/auth/login.vue";

import useAppStore from "@/store.js";

const routes = [
  { path: "/", component: HomeView, name: "home" },
  { path: "/auth/login/", component: LoginView, name: "auth-login" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  var api = new API();
  const store = useAppStore();

  if (to.name == "auth-login" || api.isAuthenticated()) {
    store.authenticated = true;
    next();
  } else {
    next({ name: "auth-login", query: { next: to.path } });
  }
});

export default router;
