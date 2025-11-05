<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'logout',
    data() {
      return {
        section: 'Head',
        auth: {
          authenticated: false,
          user: {}
        }
      }
    },
    created() {
      this.logout()
    },
    methods: {
      logout() {
        window.localStorage.removeItem('openapi-username')
        window.localStorage.removeItem('openapi-token')
        window.localStorage.removeItem('openapi-roles')
        window.localStorage.removeItem('openapi-exp')
        window.localStorage.setItem('openapi-authenticated', false);
        this.$router.push('/login')
      }
    }
  }
</script>
