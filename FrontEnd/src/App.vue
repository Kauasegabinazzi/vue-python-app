<template>
  <v-app>
    <v-main>
      <Users/>
    </v-main>
  </v-app>
</template>

<script>
import Users from './views/Users.vue'

export default {
  name: 'App',

  components: {
    Users,
  },

  data: () => ({
    //
  }),
}
</script>
