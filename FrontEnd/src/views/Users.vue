<template>
  <v-container>
    <v-btn color="primary" @click="openCreateUserDialog">Create User</v-btn>

    <v-data-table :headers="headers" :items="users" item-value="username">
      <template v-slot:item="{ item }">
        <tr>
          <td>{{ item.username }}</td>
          <td>{{ item.roles?.join(", ") }}</td>
          <td>{{ item.preferences?.timezone }}</td>
          <td>
            <v-icon v-if="item.active" color="green">mdi-check</v-icon>
            <v-icon v-else color="red">mdi-close</v-icon>
          </td>
          <td>{{ new Date(item.created_ts).toISOString().split("T")[0] }}</td>
          <td>{{ new Date(item.created_ts).toISOString().split("T")[0] }}</td>
          <td class="d-flex" style="gap: 5px">
            <v-btn color="blue" small @click="editUser(item)">Edit</v-btn>
            <v-btn color="red" small @click="deleteUser(item.username)"
              >Delete</v-btn
            >
          </td>
        </tr>
      </template>
    </v-data-table>

    <UserDialog
      v-model:dialog="dialog"
      :user="user"
      :editing="editing"
      @save-user="saveUser"
      @refresh-users="fetchUsers"
    />
  </v-container>
</template>

<script>
import api from "../api";
import UserDialog from "@/components/UserDialog.vue";

export default {
  name: "HelUloWorld",
  components: { UserDialog },
  data() {
    return {
      users: [],
      dialog: false,
      editing: false,
      user: null, 
      headers: [
        { title: "Username", key: "username" },
        { title: "Roles", key: "roles" },
        { title: "Timezone", key: "preferences.timezone" },
        { title: "Is Active?", key: "active" },
        { title: "Last Updated At", key: "created_ts" },
        { title: "Created At", key: "created_ts" },
        { title: "Actions", key: "actions", sortable: false },
      ],
    };
  },
  created() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const { data } = await api.getUsers();
        this.users = data;
      } catch (error) {
        console.error("Error searching user:", error);
      }
    },

    openCreateUserDialog() {
      this.user = {
        user: "",
        password: "",
        is_user_admin: false,
        is_user_manager: false,
        is_user_tester: false,
        user_timezone: "",
        is_user_active: true,
        created_at: new Date().toISOString(),
      };
      this.editing = false;
      this.dialog = true;
    },

    editUser(item) {
      if (confirm("Are you sure you want to edit this user?")) {
        this.user = { ...item }; 
        this.editing = true;
        this.dialog = true;
      }
    },

    async deleteUser(id) {
      if (confirm("Are you sure you want to delete this user?")) {
        try {
          await api.deleteUser(id);
          this.fetchUsers(); // update list
        } catch (error) {
          console.error("Error deleting user:", error);
        }
      }
    },
  },
};
</script>
