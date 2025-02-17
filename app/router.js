import { createWebHashHistory, createRouter } from "vue-router";

import NotFound from "@/components/not-found.vue";

import HomeView from "@/home/home.vue";
import LoginView from "@/auth/login.vue";

import FollowList from "@/follow/follow-list.vue";
import FollowInvite from "@/follow/invite.vue";
import AcceptInvite from "@/follow/accept.vue";

import useAppStore from "@/services/store.js";

const routes = [
  { path: "/", component: HomeView, name: "home" },
  { path: "/auth/login/", component: LoginView, name: "auth-login" },
  { path: "/invite/:code", component: AcceptInvite, name: "follow-accept" },
  { path: "/follow/add/", component: FollowInvite, name: "follow-invite" },
  { path: "/follow/", component: FollowList, name: "follow-list" },
  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFound },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const store = useAppStore();

  if (to.name == "auth-login") {
    next();
  } else if (store.isAuthenticated()) {
    next();
  } else {
    next({ name: "auth-login", query: { next: to.path } });
  }
});

export default router;
