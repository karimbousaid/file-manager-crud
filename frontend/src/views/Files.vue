<template>
  <div class="container py-4">
    <!-- Header -->
    <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-2 mb-3">
      <div>
        <h3 class="mb-0">Meine Dateien</h3>
        <small class="text-muted">Dateien hinzufügen, bearbeiten und löschen</small>
      </div>

      <div class="d-flex gap-2">
        <button class="btn btn-primary" @click="openAdd">
          Datei hinzufügen
        </button>
      </div>
    </div>

    <!-- Alert -->
    <div v-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>

    <!-- Table Card -->
    <div class="card shadow-sm border-0">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th style="width: 80px;">ID</th>
                <th>Dateiname</th>
                <th>Pfad</th>
                <th style="width: 170px;">Erstellt am</th>
                <th style="width: 170px;">Erstellt von</th>
                <th class="text-end" style="width: 220px;">Aktionen</th>
              </tr>
            </thead>

            <tbody>
              <!-- Loading -->
              <tr v-if="loading">
                <td colspan="6" class="text-center py-4">
                  <div class="spinner-border" role="status"></div>
                  <div class="text-muted mt-2">Lade Dateien…</div>
                </td>
              </tr>

              <!-- Empty -->
              <tr v-else-if="files.length === 0">
                <td colspan="6" class="text-center py-5">
                  <div class="fw-semibold">Keine Dateien vorhanden</div>
                  <div class="text-muted mb-3">Füge deine erste Datei hinzu.</div>
                  <button class="btn btn-primary" @click="openAdd">
                    Datei hinzufügen
                  </button>
                </td>
              </tr>

              <!-- Rows -->
              <tr v-else v-for="file in files" :key="file.id">
                <td class="text-muted">{{ file.id }}</td>

                <td>
                  <div class="fw-semibold">{{ displayName(file) }}</div>
                </td>

                <td>
                  <span class="badge text-bg-light border">
                    {{ file.filepath }}
                  </span>
                </td>

                <td class="text-muted">
                  {{ formatDate(file.upload_date || file.upload_date) }}
                </td>

                <td>
                  <span class="badge text-bg-secondary">
                    {{ file.owner_username || file.owner_username || "-" }}
                  </span>
                </td>

                <td class="text-end">
                  <button class="btn btn-outline-warning btn-sm me-2" @click="openEdit(file)">
                    Bearbeiten
                  </button>
                  <button class="btn btn-outline-danger btn-sm" @click="deleteFile(file.id)">
                    Löschen
                  </button>
                </td>
              </tr>
            </tbody>

          </table>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <FileModal
      v-if="showModal"
      :isEdit="isEdit"
      :formData="currentFile"
      @closed="showModal = false"
      @saved="afterSaved"
    />
  </div>
</template>

<script>
import FileService from "../services/FileService";
import FileModal from "../components/FileModal.vue";

export default {
  components: { FileModal },

  data() {
    return {
      files: [],
      showModal: false,
      isEdit: false,
      currentFile: {},
      loading: false,
      error: ""
    };
  },

  methods: {
    getFileNameOnly(pathOrName) {
      return (pathOrName || "").split(/[\\/]/).pop();
    },

    stripExtension(name) {
      const base = this.getFileNameOnly(name);
      const idx = base.lastIndexOf(".");
      return idx > 0 ? base.slice(0, idx) : base;
    },

    displayName(file) {
      const source = file?.filename || file?.filepath || "";
      return this.stripExtension(source) || "-";
    },

    formatDate(value) {
      if (!value) return "-";
      const d = new Date(value);
      if (isNaN(d.getTime())) return String(value);
      return d.toLocaleString("de-DE");
    },

    async loadFiles() {
      this.error = "";
      this.loading = true;

      try {
        const res = await FileService.getAll();
        this.files = res.data || [];
      } catch (e) {
        console.error(e);
        this.error = "Dateien konnten nicht geladen werden.";
      } finally {
        this.loading = false;
      }
    },

    openAdd() {
      this.isEdit = false;
      this.currentFile = { filename: "" };
      this.showModal = true;
    },

    openEdit(file) {
      this.isEdit = true;
      this.currentFile = { ...file };
      this.showModal = true;
    },

    async deleteFile(id) {
      if (!confirm("Datei wirklich löschen?")) return;

      this.error = "";
      try {
        await FileService.delete(id);
        await this.loadFiles();
      } catch (e) {
        console.error(e);
        this.error = "Löschen fehlgeschlagen.";
      }
    },

    async afterSaved() {
      this.showModal = false;
      await this.loadFiles();
    }
  },

  mounted() {
    this.loadFiles();
  }
};
</script>