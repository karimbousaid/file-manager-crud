<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow px-3">
    <div class="container-fluid">

      <router-link class="navbar-brand fw-semibold text-white" to="/files">
        File Manager Crud
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarContent"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarContent">
        <div class="ms-auto d-flex gap-2 mt-3 mt-lg-0">

          <!-- Not Logged In -->
          <template v-if="!isLogged">
            <router-link class="btn btn-outline-light" to="/login">
              Login
            </router-link>

            <router-link class="btn btn-light" to="/register">
              Register
            </router-link>
          </template>

          <!-- Logged In -->
          <template v-else>
            <button class="btn btn-outline-danger" @click="logout">
              Logout
            </button>
          </template>

        </div>
      </div>

    </div>
  </nav>
</template>

<script>
import AuthService from "../services/AuthService";

export default {
  data() {
    return { isLogged: false };
  },

  methods: {
    checkAuth() {
      this.isLogged = !!AuthService.getToken();
    },

    logout() {
      AuthService.logout();
      this.checkAuth();
      this.$router.push("/login");
    }
  },

  mounted() {
    this.checkAuth();
    window.addEventListener("storage", this.checkAuth);
  },

  watch: {
    $route() {
      this.checkAuth();
    }
  }
};
</script>