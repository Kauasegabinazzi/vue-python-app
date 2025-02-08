import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // URL backend
});

export default {
  getUsers() {
    return api.get("/users");
  },
  createUser(user) {
    return api.post("/users", user);
  },
  updateUser(id, user) {
    return api.put(`/users/${id}`, user);
  },
  deleteUser(id) {
    return api.delete(`/users/${id}`);
  },
};
