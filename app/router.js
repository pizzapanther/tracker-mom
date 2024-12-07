import { createWebHistory, createRouter } from "vue-router";

import API from "@/api.js";
import HomeView from "@/home/home.vue";
import LoginView from "@/auth/login.vue";

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

  if (to.name == "auth-login" || api.isAuthenticated()) {
    next();
  } else {
    next({ name: "auth-login", query: { next: to.path } });
  }
});

export default router;
