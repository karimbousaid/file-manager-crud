<template>
  <div
    class="modal fade"
    tabindex="-1"
    ref="modal"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">

        <!-- Header -->
        <div class="modal-header bg-primary text-white">
          <h5 class="modal-title">
            {{ isEdit ? "Datei bearbeiten" : "Datei hinzufügen" }}
          </h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            @click="closeModal"
            :disabled="loading"
          ></button>
        </div>

        <!-- Body -->
        <div class="modal-body">
          <div v-if="error" class="alert alert-danger py-2 mb-3">
            {{ error }}
          </div>

          <!-- Upload (only create mode) -->
          <div class="mb-3" v-if="!isEdit">
            <label class="form-label fw-semibold">
              Datei auswählen (nur PDF oder TXT)
            </label>
            <input
              ref="fileInput"
              type="file"
              class="form-control"
              accept=".pdf,.txt"
              @change="handleFile"
              :disabled="loading"
            />
            <div class="form-text">
              Bitte eine PDF- oder TXT-Datei auswählen.
            </div>
          </div>

          <!-- Filename -->
          <div class="mb-3">
            <label class="form-label fw-semibold">Dateiname</label>
            <input
              v-model.trim="form.filename"
              type="text"
              class="form-control"
              :readonly="!isEdit"
              placeholder="Dateiname"
            />
            <div class="form-text text-muted">
              {{ isEdit
                ? "Ändere nur den Dateinamen (Dateiendung bleibt gleich)."
                : "Der Dateiname wird automatisch aus der Datei übernommen."
              }}
            </div>
          </div>

        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <button
            class="btn btn-outline-secondary"
            @click="closeModal"
            :disabled="loading"
          >
            Abbrechen
          </button>

          <button
            class="btn btn-primary"
            @click="saveFile"
            :disabled="loading"
          >
            <span
              v-if="loading"
              class="spinner-border spinner-border-sm me-2"
            ></span>
            {{ loading ? "Speichern..." : "Speichern" }}
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from "bootstrap";
import FileService from "../services/FileService";

export default {
  name: "FileModal",

  props: {
    isEdit: { type: Boolean, default: false },
    formData: { type: Object, default: () => ({}) }
  },

  data() {
    return {
      form: {
        id: this.formData.id || null,
        filename: this.formData.filename || "",
        file: null
      },
      modal: null,
      loading: false,
      error: ""
    };
  },

  methods: {

    // helper to kee the name extension
    getExt(name) {
      const base = (name || "").split(/[\\/]/).pop();
      const index = base.lastIndexOf(".");
      return index > 0 ? base.slice(index + 1).toLowerCase() : "";
    },

    getBaseName(name) {
      const base = (name || "").split(/[\\/]/).pop();
      const index = base.lastIndexOf(".");
      return index > 0 ? base.slice(0, index) : base;
    },

    sanitizeBaseName(input) {
      const noPath = (input || "").split(/[\\/]/).pop();
      return this.getBaseName(noPath).trim();
    },

    handleFile(e) {
      const file = e.target.files?.[0];
      if (!file) return;

      const allowedExtensions = ["pdf", "txt"];
      const fileExt = this.getExt(file.name);

      if (!allowedExtensions.includes(fileExt)) {
        this.error = "Nur PDF- oder TXT-Dateien sind erlaubt!";
        this.form.file = null;
        this.form.filename = "";
        e.target.value = "";
        return;
      }

      this.error = "";
      this.form.file = file;
      this.form.filename = file.name;
    },

    closeModal() {
      if (this.loading) return;
      this.modal?.hide();
      this.$emit("closed");
    },

    async saveFile() {
      this.error = "";

      if (!this.form.filename.trim()) {
        this.error = this.isEdit
          ? "Bitte einen Dateinamen eingeben."
          : "Bitte eine Datei auswählen.";
        return;
      }

      this.loading = true;

      try {
        if (this.isEdit && this.form.id) {
          // keep original extension
          const originalExt = this.getExt(
            this.formData.filename || this.form.filename
          );

          const newBase = this.sanitizeBaseName(this.form.filename);

          if (!newBase) {
            this.error = "Ungültiger Dateiname.";
            this.loading = false;
            return;
          }

          const finalName = originalExt
            ? `${newBase}.${originalExt}`
            : newBase;

          await FileService.update(this.form.id, {
            new_name: finalName
          });
        } else {
          if (!this.form.file) {
            this.error = "Bitte eine Datei auswählen.";
            this.loading = false;
            return;
          }

          const uploadExt = this.getExt(this.form.file.name);
          const newBase = this.sanitizeBaseName(this.form.filename);
          const finalName = uploadExt
            ? `${newBase}.${uploadExt}`
            : newBase;

          const data = new FormData();
          data.append("file", this.form.file);
          data.append("new_name", finalName);

          await FileService.create(data);
        }

        this.$emit("saved");
        this.modal.hide();
      } catch (e) {
        console.error(e);
        this.error = "Speichern fehlgeschlagen. Bitte erneut versuchen.";
      } finally {
        this.loading = false;
      }
    }
  },

  mounted() {
    this.modal = new Modal(this.$refs.modal, {
      backdrop: "static",
      keyboard: false
    });

    // show only base name in edit mode
    if (this.isEdit && this.formData.filename) {
      this.form.filename = this.getBaseName(this.formData.filename);
    }

    this.modal.show();

    this.$refs.modal.addEventListener("hidden.bs.modal", () => {
      this.$emit("closed");
    });
  }
};
</script>

<style scoped>
.modal-content {
  border-radius: 0.5rem;
}
</style>