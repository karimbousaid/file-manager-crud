import API from "../api";

export default {
  getAll: () => API.get("/files"),
  create: (data) => API.post("/files", data),
  update: (id, data) => API.put(`/files/${id}`, data),
  delete: (id) => API.delete(`/files/${id}`)
};