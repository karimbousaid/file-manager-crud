<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-12 col-sm-10 col-md-6 col-lg-5">

        <div class="card shadow-sm border-0">
          <div class="card-body p-4">
            <h3 class="mb-3">Anmelden</h3>
            <p class="text-muted mb-4">Melden Sie sich an, um Ihre Dateien zu verwalten.</p>

            <div v-if="error" class="alert alert-danger py-2">
              {{ error }}
            </div>

            <form @submit.prevent="submit">
              <div class="mb-3">
                <label class="form-label">Benutzername</label>
                <input
                  v-model.trim="username"
                  type="text"
                  class="form-control"
                  placeholder="Benutzername eingeben"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Passwort</label>
                <input
                  v-model="password"
                  type="password"
                  class="form-control"
                  placeholder="Passwort eingeben"
                  required
                />
              </div>

              <button
                type="submit"
                class="btn btn-primary w-100"
                :disabled="loading"
              >
                <span
                  v-if="loading"
                  class="spinner-border spinner-border-sm me-2"
                ></span>
                {{ loading ? "Anmeldung läuft..." : "Anmelden" }}
              </button>
            </form>

            <hr class="my-4" />

            <div class="text-center">
              <span class="text-muted">Noch kein Konto?</span>
              <router-link class="ms-1" to="/register">
                Registrieren
              </router-link>
            </div>

          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import AuthService from "../services/AuthService";

export default {
  data() {
    return {
      username: "",
      password: "",
      loading: false,
      error: ""
    };
  },
  methods: {
    async submit() {
      this.error = "";

      if (!this.username || !this.password) {
        this.error = "Bitte Benutzername und Passwort eingeben.";
        return;
      }

      this.loading = true;

      try {
        await AuthService.login(this.username, this.password);
        this.$router.push("/files");
      } catch {
        this.error = "Anmeldung fehlgeschlagen. Bitte Zugangsdaten prüfen.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>