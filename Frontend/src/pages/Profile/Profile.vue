<template>
  <div class="profile-page">  
    <h2 class="page-title">Profile - <span class="fw-semi-bold">OpenAPI</span></h2>
    <Widget
      customHeader close collapse
    >
      <div class="row">
        <div class="col-md-3 border-right">
          <div class="d-flex flex-column align-items-center text-center p-3 py-5">
            <img class="rounded-circle mt-5" width="150px" :src="model.avatar">
              <span class="font-weight-bold">{{ model.username }}</span>
              <span class="text-black-50">{{ model.email }}</span><span> </span>
          </div>
        </div>
        <div class="col-md-5 border-right">
          <div class="p-3 py-5">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h4 class="text-right">Profile Settings</h4>
            </div>
            <div class="row mt-2">
              <div class="col-md-6"><label class="labels">Name</label><input type="text" class="form-control" :value="model.firstname" readonly></div>
                <div class="col-md-6"><label class="labels">Surname</label><input type="text" class="form-control" :value="model.lastname" readonly></div>
              </div>
              <div class="row mt-3">
                <div class="col-md-12"><label class="labels">Username</label><input type="text" class="form-control" :value="model.username" readonly></div>
                <div class="col-md-12"><label class="labels">Email</label><input type="text" class="form-control" :value="model.email" readonly></div>
                <div class="col-md-12"><label class="labels">Phone</label><input type="text" class="form-control" :value="model.phone" readonly></div>
                <div class="col-md-12"><label class="labels">Company</label><input type="text" class="form-control" :value="model.company" readonly></div>
                <div class="col-md-12"><label class="labels">Address</label><input type="text" class="form-control" :value="model.address" readonly></div>
              </div>
            </div>
          </div>
<!-- 
          <div class="clearfix">
            <div class="float-right">
              <b-button variant="default" class="mr-3" size="sm" v-b-modal.editProfileIndo>New</b-button>
            </div>
          </div>
-->          
        <div class="col-md-3 border-right">
          <div class="row mt-3">
            <b-badge variant="warning"><a :href="model.editProfile">Click Here to Edit Profile</a></b-badge>
          </div>
          <div class="row mt-3">
            <b-badge variant="danger"><a :href="model.changePassword">Click Here to Change Password</a></b-badge>
          </div>
          <div class="row mt-3" v-if="model.username !== 'adminapi'">
          <b-badge variant="success" v-b-modal.keyInfo @click="viewKey()">view key</b-badge>
          </div>
          <div class="row mt-3" v-if="model.username !== 'adminapi'">
            <b-badge variant="primary" v-b-modal.genKey>create key</b-badge>
          </div>
        </div>
      </div>
      <b-modal
        id="keyInfo"
        ref="modal"
        title="PublicKey/PrivateKey Info"
        scrollable
        ok-only
        @hidden="handleOKkeyInfo"
        @ok="handleOKkeyInfo"
      >
        <table class="table table-striped">
          <tbody>
            <tr>
              <td>Public Key</td>
                <td>{{ crypto_response.public_key }}
              </td>
            </tr>
              <tr>
              <td>Private Key</td>
                  <td>{{ crypto_response.private_key }}</td>
              </tr>
          </tbody>
        </table>
      </b-modal>
      <b-modal
        id="genKey"
        ref="modal"
        title="Generate PublicKey/PrivateKey"
        scrollable
        @ok="handleOKgenKey"
      >
        <div class="col-md-6"><label class="labels">Generate Key ?</label></div>
      </b-modal>
<!-- 
      <b-modal
            id="editProfileInfo"
            ref="modal"
            title="Edit Profile Info"
            scrollable
            ok-only
            @ok="handleOKeditProfileInfo"
          >
            <div class="widget-top-overlay widget-padding-md clearfix bg-info text-white">
              <div class="row mt-2">
                <div class="col-md-6"><label class="labels">Name</label><input type="text" class="form-control" :value="selectedUser.firstname" v-model="model.firstname"></div>
                <div class="col-md-6"><label class="labels">Surname</label><input type="text" class="form-control" :value="selectedUser.lastname" v-model="model.lastname"></div>
              </div>
              <div class="row mt-3">
                <div class="col-md-12"><label class="labels">Email</label><input type="text" class="form-control" :value="selectedUser.email" v-model="model.email"></div>
                <div class="col-md-12"><label class="labels">Phone</label><input type="text" class="form-control" :value="selectedUser.phone" v-model="model.phone"></div>
                <div class="col-md-12"><label class="labels">Company</label><input type="text" class="form-control" :value="selectedUser.company" v-model="model.company"></div>
                <div class="col-md-12"><label class="labels">Address</label><input type="text" class="form-control" :value="selectedUser.address" v-model="model.address"></div>
              </div>
            </div>
          </b-modal>
-->
      <b-modal
        id="sessionTimeout"
        ref="modal"
        title="Session timeout"
        ok-only
        @show="resetModal"
        @hidden="handleOKsessionTimeout"
        @ok="handleOKsessionTimeout"
      >
        <p class="my-4">Session Timeout, need relogin.</p>
      </b-modal>
      <b-modal
        id="notifResponse"
        ref="modal"
        title="Response result"
        ok-only
        @hidden="handleOKnotifResponse"
        @ok="handleOKnotifResponse"
      >
        <p class="my-4">Response from server: {{ response_error }}</p>
      </b-modal>
    </Widget>
  </div>
</template>

<script>
import axios from 'axios'
import backend from '@/server'
import jwt_decode from 'jwt-decode'

export default {
  name: 'Profile',
  data() {
    return {
      model: {
        editProfile: backend.keycloakURI + '/realms/openapi/account/#/personal-info',
        changePassword: backend.keycloakURI +  '/realms/openapi/account/#/security/signingin',
        userId: '',
        avatar: '',
        firstname: '',
        lastname: '',
        username: '',
        email: '',
        phone: '',
        company: '',
        address: ''
      },
      user_response: {},
      isLoadingUser: false,
      crypto_response: {},
      response_error: '',
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      let token = window.localStorage.getItem('openapi-token')
      let decoded_token = jwt_decode(token);
      this.model.userId = decoded_token.sub
      this.model.firstname = decoded_token.given_name
      this.model.lastname = decoded_token.family_name
      this.model.username = decoded_token.preferred_username
      this.model.email = decoded_token.email
      this.model.phone = decoded_token.ph
      this.model.company = decoded_token.company
      this.model.address = decoded_token.addr
      this.model.avatar = decoded_token.avatar
    },
    async createKey() {
      var url = backend.backendURI + '/api/v1/basecrypto'
      var token = window.localStorage.getItem('openapi-token')
      var dbody = {
        "user_id": this.model.userId,
      }
      try {
        const resp = await axios.post(url, dbody, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.crypto_response = resp.data.data
        this.response_error = 'Create Key Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingCrypto = true;
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingCrypto = true;
      } finally {
        this.isLoadingCrypto = true;
      }
    },
    async viewKey() {
      var url = backend.backendURI + '/api/v1/basecrypto/user/' + this.model.userId
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.get(url, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.crypto_response = resp.data.data
        this.isLoadingCrypto = true;
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingCrypto = true;
      } finally {
        this.isLoadingCrypto = true;
      }
    },
    async editProfileInfo() {
      var url = backend.backendURI + '/api/v1/user/' + this.model.userId
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.put(url, {
                "firstname": this.model.firstname,
                "lastname": this.model.lastname,
                "email": this.model.email,
                "phone": this.model.phone,
                "company": this.model.company,
                "address": this.model.address,
                "avatar": this.model.avatar
            }, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.user_response = resp.data.data
        this.response_error = 'Edit Profile Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingUser = true;
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingUser = true;
      } finally {
        this.isLoadingUser = true;
      }
    },
    resetModal() {
      this.model.userId = ''
      this.model.avatar = ''
      this.model.firstname = ''
      this.model.lastname = ''
      this.model.username = ''
      this.model.email = ''
      this.model.phone = ''
      this.model.company = ''
      this.model.address = ''
    },
    handleOKsessionTimeout(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmitsessionTimeout();
    },
    handleSubmitsessionTimeout() {
      this.$nextTick(() => {
        this.$router.push('/logout')
        this.$bvModal.hide('sessionTimeout');
      })
    },
    handleOKnotifResponse(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmitnotifResponse();
    },
    handleSubmitnotifResponse() {
      this.$nextTick(() => {
        this.$bvModal.hide('notifResponse');
      })
    },
    handleOKkeyInfo(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmitkeyInfo();
    },
    handleSubmitkeyInfo() {
      this.$nextTick(() => {
        this.$bvModal.hide('keyInfo');
      })
    },
    handleOKgenKey(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmitgenKey();
    },
    handleSubmitgenKey() {
      this.$nextTick(() => {
        this.createKey()
        this.$bvModal.hide('genKey');
      })
    },
    handleOKeditProfileInfo(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmiteditProfileInfo();
    },
    handleSubmiteditProfileInfo() {
      this.$nextTick(() => {
        this.editProfileInfo();
        this.$bvModal.hide('editProfileInfo');
      })
    },
  },
  computed: {
  }
};
</script>

<style src="./Profile.scss" lang="scss" />
