<template>
  <div class="tenants-page">
    <h2 class="page-title">Tenants - <span class="fw-semi-bold">OpenAPI</span></h2>
    <b-row>
      <b-col>
        <Widget
          title="<h5>Tenant <span class='fw-semi-bold'>List</span></h5>"
          customHeader close collapse
        >
          <div class="table-resposive">
            <b-skeleton-table v-if="!dataReady"
              :rows="3"
              :columns="4"
              :table-props="{ bordered: true, striped: true }"
              :loading="dataReady"
            ></b-skeleton-table>
              <table v-else class="table">
                <thead>
                  <tr>
                    <th>Avatar</th>
                    <th>Username</th>
                    <th class="hidden-sm-down">Firstname</th>
                    <th class="hidden-sm-down">Lastname</th>
                    <th class="hidden-sm-down">Phone</th>
                    <th class="hidden-sm-down">Email</th>
                    <th class="hidden-sm-down">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, index) in users_response" :key="row.db_id">
                    <td>
                     <img class="img-rounded" :src="getImgUrl(row.avatar)" alt="" height="50" />
                    </td>
                    <td>
                      {{row.username}}
                      <br>
                      <b-badge variant="info" v-b-modal.profileInfo @click="profileUser(index)"><small>detail</small></b-badge>
                    </td>
                    <td>
                      {{row.firstname}}
                    </td>
                    <td class="text-semi-muted">
                      {{row.lastname}}
                    </td>
                    <td class="text-semi-muted">
                      {{row.phone}}
                    </td>
                    <td class="text-semi-muted">
                      {{row.email}}
                    </td>
                    <td>
                      <b-badge variant="primary" v-b-modal.keyInfo @click="viewKey(row.user_id)"><small>view key</small></b-badge>
                      <br>
                      <b-badge variant="warning" v-b-modal.genKey @click="profileUser(index)"><small>create key</small></b-badge>
                      <br>
                      <b-badge v-if="row.isactive === true" variant="danger" v-b-modal.enableUser @click="profileUser(index)"><small>disable user</small></b-badge>
                      <b-badge v-if="row.isactive === false" variant="danger" v-b-modal.enableUser @click="profileUser(index)"><small>enable user</small></b-badge>
                    </td>
                  </tr>
                </tbody>
              </table>
          </div>
          <div class="clearfix">
            <div class="float-right">
              <b-button variant="default" class="mr-3" size="sm" v-b-modal.newTenant>New</b-button>
            </div>
            <p><p>Tenants Registration</p></p>
          </div>
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
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKnotifResponse"
          >
            <p class="my-4">Response from server: {{ response_error }}</p>
          </b-modal>
          <b-modal
            id="keyInfo"
            ref="modal"
            title="PublicKey/PrivateKey Info"
            scrollable
            ok-only
            @show="resetModal"
            @hidden="resetModal"
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
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKgenKey"
          >
              <div class="col-md-6"><label class="labels">Generate Key ?</label></div>
          </b-modal>
          <b-modal
            id="enableUser"
            ref="modal"
            title="Disable/Enable User"
            scrollable
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKenableUser"
          >
            <div v-if="selectedUser.isactive === true" class="col-md-6"><label class="labels">Disable User ?</label></div>
            <div v-else class="col-md-6"><label class="labels">Enable User ?</label></div>
          </b-modal>
          <b-modal
            id="profileInfo"
            ref="modal"
            title="Profile Info"
            scrollable
            ok-only
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKprofileInfo"
          >
            <div v-if="Object.entries(selectedUser).length !== 0">
              <div class="widget-top-overlay widget-padding-md clearfix bg-info text-white">
                <div class="row mt-2">
                  <div class="col-md-6"><label class="labels">Name</label><input type="text" class="form-control" :value="selectedUser.firstname" readonly></div>
                  <div class="col-md-6"><label class="labels">Surname</label><input type="text" class="form-control" :value="selectedUser.lastname" readonly></div>
                </div>
                <div class="row mt-3">
                  <div class="col-md-12"><label class="labels">Username</label><input type="text" class="form-control" :value="selectedUser.username" readonly></div>
                  <div class="col-md-12"><label class="labels">Email</label><input type="text" class="form-control" :value="selectedUser.email" readonly></div>
                  <div class="col-md-12"><label class="labels">Phone</label><input type="text" class="form-control" :value="selectedUser.phone" readonly></div>
                  <div class="col-md-12"><label class="labels">Company</label><input type="text" class="form-control" :value="selectedUser.company" readonly></div>
                  <div class="col-md-12"><label class="labels">Address</label><input type="text" class="form-control" :value="selectedUser.address" readonly></div>
                  <div class="col-md-12"><label class="labels">Since</label><input type="text" class="form-control" :value="selectedUser.created_at" readonly></div>
                </div>
              </div>
            </div>
          </b-modal>        
          <b-modal
            id="newTenant"
            ref="modal"
            title="Create New Tenant"
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKnewTenant"
          >
            <form ref="form" @submit.stop.prevent="handleSubmitnewTenant">
              <b-form-group
                label="Username"
                label-for="username-input"
                invalid-feedback="Username is required"
                :state="model.usernameState"
              >
                <b-form-input
                  id="username-input"
                  v-model="model.username"
                  :state="model.usernameState"
                  required
                ></b-form-input>
              </b-form-group>
              <b-form-group
                label="Password"
                label-for="password-input"
                invalid-feedback="Password is required"
                :state="model.passwordState"
              >
                <b-form-input
                  id="password-input"
                  v-model="model.password"
                  :state="model.passwordState"
                  required
                ></b-form-input>
              </b-form-group>
              <b-form-group
                label="Firstname"
                label-for="firstname-input"
                invalid-feedback="Firstname is required"
                :state="model.firstnameState"
              >
                <b-form-input
                  id="firstname-input"
                  v-model="model.firstname"
                  :state="model.firstnameState"
                  required
                ></b-form-input>
              </b-form-group>
              <b-form-group
                label="Lastname"
                label-for="lastname-input"
                invalid-feedback="Lastname is required"
                :state="model.lastnameState"
              >
                <b-form-input
                  id="lastname-input"
                  v-model="model.lastname"
                  :state="model.lastnameState"
                  required
                ></b-form-input>
              </b-form-group>
              <b-form-group
                label="Email"
                label-for="email-input"
                invalid-feedback="Email is required"
                :state="model.emailState"
              >  
                <b-form-input
                  id="email-input"
                  v-model="model.email"
                  :state="model.emailState"
                  required
                ></b-form-input>
              </b-form-group>
              <b-form-group
                label="Phone"
                label-for="phone-input"
                invalid-feedback="Phone is required"
                :state="model.phoneState"
              >  
                <b-form-input
                  id="phone-input"
                  v-model="model.phone"
                  :state="model.phoneState"
                  required
                ></b-form-input>
              </b-form-group>  
              <b-form-group
                label="Company"
                label-for="company-input"
                invalid-feedback="Company is required"
                :state="model.companyState"
              >  
                <b-form-input
                  id="company-input"
                  v-model="model.company"
                  :state="model.companyState"
                  required
                ></b-form-input>
              </b-form-group> 
              <b-form-group
                label="Address"
                label-for="address-input"
                invalid-feedback="Address is required"
                :state="model.addressState"
              >  
                <b-form-input
                  id="address-input"
                  v-model="model.address"
                  :state="model.addressState"
                  required
                ></b-form-input>
              </b-form-group>
<!-- 
              <b-form-group
                label="Avatar"
                label-for="avatar-input"
                invalid-feedback="Avatar is required"
                :state="model.avatarState"
              >
                <b-button variant="info" size="sm" class="mb-2 mr-2 mt-3" @click="uploadImageFile">upload</b-button>
                <span class="input-group-btn">
                  <b-form-file
                    id="avatar-input"
                    v-model="model.avatar"
                    :state="Boolean(model.avatar)"
                    accept=".jpg, .png, .gif"
                    placeholder="Choose a file or drop it here..."
                    drop-placeholder="Drop file here..."
                    ref="file-image"
                  ></b-form-file>
                </span>
              </b-form-group>
-->
            </form>
<!-- 
            <div v-if="!uploadReady" class="row justify-content-center align-items-center position-relative">
              <img v-bind:src="imagePreview" v-show="showPreview" alt="Profile Image" class="img-thumbnail" width="150">
              <div v-else class="col-md-12"><span class="fw-semi-bold">None File</span></div>
            </div>
            <div v-else class="row justify-content-center align-items-center position-relative">
              <i class="fa fa-spinner fa-spin fa-3x fa-fw"></i>
-->            
          </b-modal>
        </Widget>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import axios from 'axios'
import backend from '@/server'
import Widget from '@/components/Widget/Widget';

export default {
  name: 'Tenants',
  components: {
    Widget
  },
  data() {
    return {
      model: {
        publicKey:'',
        privateKey:'',
        userid:'',
        password:'',
        username:'',
        firstname: '',
        lastname:'',
        email:'',
        phone:'',
        company:'',
        address:'',
        rolecode:'T',
        isactive: true,
        avatar:'https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg',
        usernameState: null,
        firstnameState: null,
        lastnameState: null,
        emailState: null,
        phoneState: null,
        companyState: null,
        addressState: null,
        rolecodeState: null,
        isactiveState: null,
        avatarState: null,
        imageurl: '',
      },
      isactiveoptions: [
          { value: 'true', text: 'True' },
          { value: 'false', text: 'False' },
      ],
      showPreview: false,
      imageUploadError: '',
      uploadingImage: false,
      loadingUpload: false,
      imagePreview: '',
      isLoading: false,
      isLoadingCrypto: false,
      isLoadingUser: false,
      isLoadingTenant: false,
      selectedUser: {},
      users_response: [],
      users_response_error: {},
      user_response: {},
      tenants_response: {},
      tenants_response_error: {},
      crypto_response: {},
      response_error: '',
      upload_response: {},
      upload_response_error: {},
    };
  },
  created() {
    this.load();
  },
  methods: {
    load() {
      this.getTenants();
    },
    getImgUrl(path) {
      return backend.minioURI + path
    },
    async profileUser(index) {
      this.selectedUser = this.users_response[index];
    },
    async createKey(userid) {
      var url = backend.backendURI + '/api/v1/basecrypto'
      var token = window.localStorage.getItem('openapi-token')
      var dbody = {
        "user_id": userid,
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
    async enableUser(userid, status) {
      var url = backend.backendURI + '/api/v1/user/enable' + userid
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.put(url, {
        params: {
          "enable": status,
        }}, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.user_response = resp.data.data
        this.response_error = 'Enable/Disable User Success'
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
    async viewKey(userid) {
      var url = backend.backendURI + '/api/v1/basecrypto/user/' + userid
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
    async getTenants() {
      var url = backend.backendURI + '/api/v1/user/all?order_type=ASC&limit=100&page=1'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.get(url, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.users_response = resp.data.data
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
    async createNewTenant() {
      var url = backend.backendURI + '/api/v1/user'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.post(url, {
                "user_id": "0000-0000-0000",
                "username": this.model.username,
                "password": this.model.password,
                "firstname": this.model.firstname,
                "lastname": this.model.lastname,
                "email": this.model.email,
                "phone": this.model.phone,
                "company": this.model.company,
                "address": this.model.address,
                "rolecode": "T",
                "isactive": true,
                "avatar": this.model.avatar
            },{
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token,
            }}
        );
        this.tenants_response = resp.data
        this.response_error = 'Create Tenant Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingUser = true;
        this.getTenants();
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
    uploadImageFile(){
      this.showPreview = false;
      this.file = this.$refs['file-image'].files[0];
      let reader  = new FileReader();
      reader.addEventListener("load", function () {
        let formData = new FormData();
        formData.append('file', this.file);
        this.putImageFile(formData);

        this.showPreview = true;
        this.imagePreview = reader.result;
      }.bind(this), false);
      if( this.file ){
        if ( /\.(jpe?g|png|gif)$/i.test( this.file.name ) ) {
          reader.readAsDataURL( this.file );
        }
      }
    },
    async putImageFile(imageData) {
      this.loadingUpload = true;
      this.uploadingImage = false
      this.imageUploadError = "";
      var url = backend.backendURI + '/api/v1/upload/image'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.post(url, imageData, {
          headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'multipart/form-data',
            }}
        );
        this.upload_response = resp.data
        this.model.avatar = this.upload_response.data.url
        this.response_error = 'Upload Image Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.loadingUpload = false;
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          console.log("Status: " + err.response.status)
        }
        this.loadingUpload = false;
      }    
    },
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity()
      this.model.usernameState  = valid
      this.model.firstnameState  = valid
      this.model.lastnameState  = valid
      this.model.emailState  = valid
      this.model.phoneState  = valid
      this.model.companyState  = valid
      this.model.addressState  = valid
      this.model.rolecodeState  = valid
      this.model.isactiveState  = valid
      // this.model.avatarState  = valid
      return valid
    },
    resetModal() {
      this.model.username = ''
      this.model.password = ''
      this.model.firstname = ''
      this.model.lastname = ''
      this.model.email = ''
      this.model.phone = ''
      this.model.company = ''
      this.model.address = ''
      this.model.rolecode ='T'
      this.crypto_response = {}
      this.model.isactive = true
      // this.model.avatar = ''
      this.model.usernameState = null
      this.model.firstnameState = null
      this.model.lastnameState = null
      this.model.emailState = null
      this.model.phoneState = null
      this.model.companyState = null
      this.model.addressState = null
      this.model.rolecodeState = null
      this.model.isactiveState = null
      // this.model.avatarState = null
      // this.model.imageurl = ''
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
        this.createKey(this.selectedUser.user_id)
        this.$bvModal.hide('genKey');
      })
    },
    handleOKprofileInfo(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmitprofileInfo();
    },
    handleSubmitprofileInfo() {
      this.$nextTick(() => {
        this.$bvModal.hide('profileInfo');
      })
    },
    handleOKenableUser(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmitenableUser();
    },
    handleSubmitenableUser() {
      this.$nextTick(() => {
        if (this.selectedUser.isactive == true) {
          this.enableUser(this.selectedUser.user_id, false);
        } else {
          this.enableUser(this.selectedUser.user_id, true);
        }
        this.$bvModal.hide('enableUser');
      })
    },
    handleOKnewTenant(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmitnewTenant();
    },
    handleSubmitnewTenant() {
      if (!this.checkFormValidity()) {
        return
      }
      this.$nextTick(() => {
        this.createNewTenant();
        this.$bvModal.hide('newTenant');
      })
    },
  },
  computed: {
    dataReady() {
      return this.isLoadingUser
    },
    uploadReady() {
      return this.loadingUpload && this.showPreview
    }
  }
};
</script>

<style src="./Tenants.scss" lang="scss" />
