// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Files from "../views/Files.vue";
import AuthService from "../services/AuthService";

const routes = [
  { path: "/login", component: Login, meta: { guestOnly: true } },
  { path: "/register", component: Register, meta: { guestOnly: true } },
  { path: "/files", component: Files, meta: { requiresAuth: true } },
  { path: "/", redirect: "/files" }
];

const router = createRouter({ history: createWebHistory(), routes });

router.beforeEach((to, from, next) => {
  const token = AuthService.getToken();

  if (to.meta.guestOnly && token) return next("/files");

  if (to.meta.requiresAuth && !token) return next("/login");

  return next();
});

export default router;