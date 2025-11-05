<template>  
  <div class="d-md-flex half">
    <div class="bg" :style="{'background-color': '#B7282D', 'background-image': 'url(' + require('../../assets/images/Vector.png') + ')'}"></div>
    <div class="contents">

      <div class="container">
        <div class="row align-items-center justify-content-center">
          <div class="col-md-12">
            <div class="form-block mx-auto">
              <div class="text-center mb-5">
                <h3 class="text-uppercase">Signin to </h3>
                <h3 class="text-uppercase"><strong>POS OPENAPI</strong></h3>
              </div>
              <form>
                <div class="form-group first">
                  <label for="username">Username</label>
                  <input type="text" class="form-control" placeholder="username" v-model="name">
                </div>
                <div class="form-group last mb-3">
                  <label for="password">Password</label>
                  <input type="password" class="form-control" placeholder="Your Password" v-model="password">
                </div>
                
                <div class="d-sm-flex mb-2 align-items-center">
                  <label class="control control--checkbox mb-3 mb-sm-0"><span class="caption">Remember me</span>
                    <input type="checkbox" checked="checked"/>
                    <div class="control__indicator"></div>
                  </label>
                  <span class="ml-auto"><a href="#/forgottenpassword" class="forgot-pass">Forgot Password</a></span> 
                </div>
                <div class="d-flex justify-content-center mb-2">
                  <center><i  v-show="loading" class="fa fa-spinner fa-spin fa-3x"></i></center>
                  <!-- errors -->
                  <div v-if=errorMessage class="alert alert-warning alert-dismissible fade show" role="alert">
                    <strong>{{errorMessage}}</strong>
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>
                </div>

                <input type="button" value="Sign in" class="btn btn-block py-2 btn-primary h5" @click="checkCreds()">                
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>    
</template>    

<script>
import Vue from 'vue'
import api from '@/api'
import jwt_decode from 'jwt-decode'
import axios from 'axios'
import backend from '@/server'

var OPENAPI_LOCAL_STORAGE_TOKEN_KEY = 'openapi-token'

export default {
  name: "login-page",
  data() {
    return {
      section: 'Login',
      name: '',
      password: '',
      response: '',
      submitted: false,
      hidePassword: true,
      usersReady: false,
      result: '',
      user_response: {},
      loading: false,
      errorMessage: ''
    }
  },
  created() {
  },
  computed: {
    passwordType() {
      return this.hidePassword ? 'password' : 'text'
    },
    passwordIcon() {
      return this.hidePassword ? 'fa-eye' : 'fa-eye-slash'
    }
  },
  methods: {
    sleep(ms) {
      return new Promise((resolve) => {
        setTimeout(resolve, ms);
      });
    },
    checkCreds() {
      this.loading = true
      this.resetResponse()
      localStorage.removeItem('openapi-username')
      localStorage.removeItem('openapi-token')
      var url = backend.backendURI + "/api/v1/sso/token"
      const data = {
        "username": this.name,
        "password": this.password
      }
      const headers = {
        "Content-Type": "application/json",
      }
      axios.post(url, data, { headers })
      .then(response => {
        var ddata = response.data
        if (ddata.status != "00") {
          this.response = 'Username/Password does not match. Please try again.'
          this.loading = false
          return
        } else {
          this.user_response = ddata.data
          var decoded_token = jwt_decode(this.user_response.access_token);
          window.localStorage.setItem('openapi-authenticated', true);
          window.localStorage.setItem('openapi-token', this.user_response.access_token);
          window.localStorage.setItem('openapi-refreshtoken', this.user_response.refresh_token);
          window.localStorage.setItem('openapi-roles', decoded_token.resource_access['adminapi'].roles);
          window.localStorage.setItem('openapi-username', decoded_token.preferred_username);
          window.localStorage.setItem('openapi-exp', decoded_token.exp);
        
          this.loading = false;
          let roles = window.localStorage.getItem('openapi-roles')
          if (roles == "admin") {
            this.$router.push('app/home');
            return
          } else if (roles == "tenant") {
            this.$router.push('tenant/home');
            return
          } else {
            this.$router.push('denied');
            return
          }
        }
      })
      .catch(error => {
          this.errorMessage = "Login failed with error: " + error.message;
          console.error("There was an error!", error);
          this.loading = false;
      })
    },
    resetResponse() {
      this.errorMessage = ''
    }
  }
}
</script>

<style src="./fonts/icomoon/style.css" lang="css" scoped />
<style src="./css/owl.carousel.min.css" lang="css" scoped />
<style src="./css/bootstrap.min.css" lang="css" scoped />
<style src="./css/style.css" lang="css" scoped />
