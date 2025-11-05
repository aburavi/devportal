<template>
  <router-view />
</template>

<script>
import jwt_decode from 'jwt-decode'
import axios from 'axios'
import backend from '@/server'

export default {
  name: "App",
  data() {
    return {
      timer: '',
      user_response: {}
    }
  },
  created() {
    let roles = window.localStorage.getItem('openapi-roles');
    this.timer = setInterval(this.refreshToken, 10000);
    if (roles) {
      if (roles.indexOf('admin') != -1) {
        this.$router.push('/app/home');
      } else if (roles.indexOf('tenant') != -1) {
        this.$router.push('/tenant/home');
      } else {
        this.$router.push("/denied");
      }
    } else {
      this.$router.push('/login', () => {});
    }
  },
  methods: {
      async refreshToken() {
        let ex_token = window.localStorage.getItem('openapi-token')
        let ex_decoded_token = jwt_decode(ex_token);
        let exp = (ex_decoded_token.exp * 1000) - 250000
        let current = Date.now();
        console.log("exp: " + exp + ", " + "current: " + current)
        if (exp < current) {
          console.log("refreshToken: token refreshed ...")
          var url = backend.backendURI + "/api/v1/sso/refresh-token"
          let token = window.localStorage.getItem('openapi-token')
          let refreshtoken = window.localStorage.getItem('openapi-refreshtoken')
          const data = {
            "refresh_token": refreshtoken
          }
          const headers = {
            "Content-Type": "application/json",
          }
          try {
            const resp = await axios.post(url, data, {
              headers: {
                'Authorization': 'Bearer ' + ex_token,
                'Content-Type': 'application/json',
              }
            });
            this.user_response = resp.data.data
            var decoded_token = jwt_decode(this.user_response.access_token);
            window.localStorage.setItem('openapi-authenticated', true);
            window.localStorage.setItem('openapi-token', this.user_response.access_token);
            window.localStorage.setItem('openapi-refreshtoken', this.user_response.refresh_token);
            window.localStorage.setItem('openapi-roles', decoded_token.resource_access['adminapi'].roles);
            window.localStorage.setItem('openapi-username', decoded_token.preferred_username);
            window.localStorage.setItem('openapi-exp', decoded_token.exp);
          } catch (err) {
            console.log("refreshToken: error refresh token, try next ...")
          }
        } else {
          console.log("refreshToken: skipped for refresh token ...")
        }
      },
      cancelAutoUpdate () {
        clearInterval(this.timer);
      }
  },
  beforeDestroy () {
    this.cancelAutoUpdate();
  },
};
</script>

<style src="./styles/theme.scss" lang="scss" />
