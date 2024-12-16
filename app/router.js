import { createWebHistory, createRouter } from "vue-router";

import API from "@/api.js";

import NotFound from "@/components/not-found.vue";

import HomeView from "@/home/home.vue";
import LoginView from "@/auth/login.vue";

import FollowList from "@/follow/follow-list.vue";
import FollowInvite from "@/follow/invite.vue";

import useAppStore from "@/store.js";

const routes = [
  { path: "/", component: HomeView, name: "home" },
  { path: "/auth/login/", component: LoginView, name: "auth-login" },
  { path: "/follow/add/", component: FollowInvite, name: "follow-invite" },
  { path: "/follow/", component: FollowList, name: "follow-list" },
  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFound },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  var api = new API();
  const store = useAppStore();

  if (to.name == "auth-login") {
    next();
  } else if (api.isAuthenticated()) {
    store.authenticated = true;
    next();
  } else {
    next({ name: "auth-login", query: { next: to.path } });
  }
});

export default router;
