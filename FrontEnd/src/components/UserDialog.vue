<template>
  <v-dialog v-model="internalDialog" max-width="500px">
    <v-card>
      <v-card-title>{{ editing ? "Edit User" : "Create User" }}</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="users.username"
                label="Username"
                prepend-icon="mdi-account"
                :disabled="editing"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="users.password"
                label="Password"
                type="password"
                prepend-icon="mdi-lock"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="users.user_timezone"
                label="Timezone"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-divider></v-divider>
              <v-subheader>Roles</v-subheader>
              <v-row>
                <v-col cols="4">
                  <v-checkbox
                    v-model="users.is_user_admin"
                    label="Admin"
                  ></v-checkbox>
                </v-col>
                <v-col cols="4">
                  <v-checkbox
                    v-model="users.is_user_manager"
                    label="Manager"
                  ></v-checkbox>
                </v-col>
                <v-col cols="4">
                  <v-checkbox
                    v-model="users.is_user_tester"
                    label="Tester"
                  ></v-checkbox>
                </v-col>
              </v-row>
            </v-col>
            <v-col cols="12">
              <v-divider></v-divider>
              <v-checkbox
                v-model="users.is_user_active"
                label="Active"
                color="success"
              ></v-checkbox>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="saveUser">Save</v-btn>
        <v-btn color="grey" @click="closeDialog">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import api from "../api";

export default {
  props: {
    dialog: Boolean,
    user: Object,
    editing: Boolean,
  },
  emits: ["update:dialog", "save-user", "refresh-users"],
  data() {
    return {
      users: {
        username: "",
        password: "",
        is_user_admin: false,
        is_user_manager: false,
        is_user_tester: false,
        user_timezone: "",
        is_user_active: false,
        created_at: "",
      },
    };
  },
  computed: {
    internalDialog: {
      get() {
        return this.dialog;
      },
      set(value) {
        this.$emit("update:dialog", value);
      },
    },
  },
  watch: {
    user: {
      handler(newUser) {
        if (newUser) {
          this.users.username = newUser.username || "";
          this.users.password = newUser.password || "";
          this.users.is_user_admin = this.editing
            ? newUser.roles.includes("admin")
            : newUser.is_user_admin || false;
          this.users.is_user_manager = this.editing
            ? newUser.roles.includes("manager")
            : newUser.is_user_manager || false;
          this.users.is_user_tester = this.editing
            ? newUser.roles.includes("tester")
            : newUser.is_user_tester || false;
          this.users.user_timezone = this.editing
            ? newUser.preferences?.timezone
            : newUser.user_timezone || "";
          this.users.is_user_active = newUser.active ?? false;
          this.users.created_at = newUser.created_at || "";
        } else {
          this.resetUser();
        }
      },
      immediate: true,
      deep: true,
    },
  },

  methods: {
    async saveUser() {
      const userPayload = {
        user: this.users.username,
        password: this.users.password,
        is_user_admin: this.users.is_user_admin,
        is_user_manager: this.users.is_user_manager,
        is_user_tester: this.users.is_user_tester,
        user_timezone: this.users.user_timezone,
        is_user_active: this.users.is_user_active,
        created_at: new Date().toISOString().split(".")[0] + "Z",
      };

      try {
        if (this.editing) {
          await api.updateUser(this.users.username, userPayload);
        } else {
          await api.createUser(userPayload);
        }
        this.internalDialog = false;
        this.$emit("refresh-users"); // update list
      } catch (error) {
        console.error("Error saving user:", error);
      }
    },
    closeDialog() {
      this.internalDialog = false;
    },
    resetUser() {
      this.users = {
        username: "",
        password: "",
        is_user_admin: false,
        is_user_manager: false,
        is_user_tester: false,
        user_timezone: "",
        is_user_active: false,
        created_at: "",
      };
    },
  },
};
</script>
