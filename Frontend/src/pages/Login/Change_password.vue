<template>  
  <div class="d-md-flex half">
    <div class="bg" :style="{'background-image': 'url(' + require('../../assets/images/bg_1.jpg') + ')'}"></div>
    <div class="contents">

      <div class="container">
        <div class="row align-items-center justify-content-center">
          <div class="col-md-12">
            <div class="form-block mx-auto">
              <div class="text-center mb-5">
                <h3 class="text-uppercase">Change Password Request</h3>
                <h3 class="text-uppercase"><strong>OpenApi POS</strong></h3>
              </div>
              <form>
                <div class="input-group last mb-3">
                  <div class="input-group-prepend">
                    <span class="input-group-text bg-white px-4 border-md border-right-0">
                      <i class="fa fa-lock text-muted"></i>
                    </span>
                  </div>
                  <input type="password" class="form-control border-left-0 border-md" placeholder="Current Password" v-model="password">
                </div>
                <div class="input-group last mb-3">
                  <div class="input-group-prepend">
                    <span class="input-group-text bg-white px-4 border-md border-right-0">
                      <i class="fa fa-lock text-muted"></i>
                    </span>
                  </div>
                  <input type="password" class="form-control border-left-0 border-md" placeholder="New Password" v-model="cpassword">
                </div>                
                <div class="input-group last mb-3">
                  <div class="input-group-prepend">
                    <span class="input-group-text bg-white px-4 border-md border-right-0">
                      <i class="fa fa-lock text-muted"></i>
                    </span>
                  </div>
                  <input type="password" class="form-control border-left-0 border-md" placeholder="Confirm New Password" v-model="rpassword">
                </div>
                <div class="d-flex justify-content-center mb-2">
                  <center><i  v-show="loading" class="fa fa-spinner fa-spin fa-3x"></i></center>
                  <!-- errors -->
                  <div v-if=response class="alert alert-warning alert-dismissible fade show" role="alert">
                    <strong>{{response}}</strong>
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>
                </div>

                <input type="submit" value="Submit New Password" class="btn btn-block py-2 btn-primary" @click="changepassword()">

              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>    
</template>    

<script>
import api from '@/api'

export default {
  name: "change-password-page",
  components: {
  },
  data() {
    return {
      userReady: false,
      error: false,
      response_error: '',
      password: '',
      cpassword:'',
      rpassword:'',
      loading: false,
      signuperror: false,
      listQuery: {
        offset: 0,
        limit: 25
      },
      auth: {
        authenticated: false,
        user: {}
      }
    }
  },
  computed: {
    dataReady() {
      return this.userReady
    }
  },
  methods: {
    changepassword() {
      this.loading = true
      if (this.password !== this.cpassword) {
	this.response_error = 'Error both password not match. Please try again.'
        this.error = true
        this.loading = false
        return
      }
      /* Making API call to authenticate a user */
      api
        .request('post', '/api/v1/user/changepassword/' + this.$route.params.token , { "authid":this.password })
        .then(response => {
          var data = response.data
          /* Checking if error object was returned from the server */
          if (data.error) {
            var errorName = data.error.name
            if (errorName) {
              this.signup_error = 'Error created new account. Please try again.'
            } else {
              this.signup_error = data.error
            }
            this.loading = false
            this.error =  false
            // alert('Failed to reset account, please try next time ' + data.error.name)
            return
          }
          this.loading = false
          this.error = false
          this.userReady = true
          this.response = 'Your Password has been change, Please keep your Account securely'
          // alert('Your Password has been change ')
          this.$router.push(data.redirect ? data.redirect : '/login')
        })
        .catch(error => {
          this.response = 'Error created new account. Please try again.' + error.response
          // alert('Failed to reset account, please try next time')
          this.loading = false
          this.error = false
        })
    }
  }
}
</script>
<style src="./fonts/icomoon/style.css" lang="css" scoped />
<style src="./css/owl.carousel.min.css" lang="css" scoped />
<style src="./css/bootstrap.min.css" lang="css" scoped />
<style src="./css/style.css" lang="css" scoped />
