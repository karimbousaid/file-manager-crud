import API from "../api";

export default {
  login: async (username, password) => {
    const res = await API.post("/auth/login", { username, password });
    localStorage.setItem("access_token", res.data.access_token);
    return res.data;
  },

  register: async (username, password) => {
    const res = await API.post("/auth/register", { username, password });
    return res.data;
  },

  logout: () => localStorage.removeItem("access_token"),

  getToken: () => localStorage.getItem("access_token")
};