<template>
  <div>
    <!-- Conditional rendering for the navbar -->
    <nav v-if="showNavbar">
      <router-link to="/">Home</router-link> |
      <router-link to="/login">Login</router-link> |
      <router-link to="/register">Register</router-link> |
      <router-link to="/about">About</router-link> 
      <button @click="logout">Logout</button>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      showNavbar: false, // Controls the visibility of the navbar
    };
  },
  methods: {
    logout() {
      localStorage.clear();
      this.showNavbar = false; // Hide the navbar on logout
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>