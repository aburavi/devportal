<template>
  <div class="documentations-page">
    <h2 class="page-title">Documentations - <span class="fw-semi-bold">OpenAPI</span></h2>
    <b-row>
      <div class="pb-xlg h-100">
        <Widget
          title="<h5>Selamat Datang Developer <small class='text-muted'> POS OpenAPI Site</small></h5>"
          customHeader close collapse
        >
          <ul>
            <li>Flow POS OpenAPI
              <div class="row">
                <div class="col-md-8 p-2 grey">
                  <img src="../../assets/images/doc/flow-openapi.png" class="img-fluid mx-auto" alt="...">
                </div>
              </div>
            </li>
          </ul>
          <p><strong>Roles Admin</strong></p>
          <p>Features:</p>
          <p>Admin Profile</p>
          <p style="margin-left: 20px;">Deskripsi: Profile admin user</p>
          <ul>
            <li>Edit Profile
              <div class="row">
                <div class="col-md-8 p-2 grey">
                  <img src="../../assets/images/doc/profile.png" class="img-fluid mx-auto" alt="...">
                </div>
              </div>
            </li>
            <li>Change password&nbsp;</li>
          </ul>
          <p>Tenant Registration</p>
          <p style="margin-left: 20px;">Deskripsi: Registration for new tenant</p>
          <ul>
            <li>Tenant List
              <div class="row">
                <div class="col-md-8 p-2 grey">
                  <img src="../../assets/images/doc/tenant_list.png" class="img-fluid mx-auto" alt="...">
                </div>
              </div>
            </li>
            <li>Generate public and private key for each tenant
              <div class="row">
                <div class="col-md-8 p-2 grey">            
                  <img src="../../assets/images/doc/generate_key.png" class="img-fluid mx-auto" alt="...">
                </div>
              </div>
            </li>
            <li>Show public and privately for each tenant
              <div class="row">
                <div class="col-md-8 p-2 grey">  
                  <img src="../../assets/images/doc/view_key.png" class="img-fluid mx-auto" alt="...">
                </div>
              </div>
            </li>
            <li>Enable/disable tenant&nbsp;</li>
          </ul>
          <p>Create Apps for each tenant</p>
          <p style="margin-left: 20px;">Deskripsi: Registration for new apps</p>
          <ul>
            <li>Apps List
              <div class="row">
                <div class="col-md-8 p-2 grey">  
                  <img src="../../assets/images/doc/apps_list.png" class="img-fluid mx-auto" alt="...">
                </div>
              </div>
            </li>
            <li>New Apps
              <div class="row">
                <div class="col-md-8 p-2 grey">  
                  <img src="../../assets/images/doc/new_apps.png" class="img-fluid mx-auto" alt="...">
                </div>
              </div>
            </li>
          </ul>
          <p>SIT-Request</p>
          <p style="margin-left: 20px;">Deskripsi: Registration for SIT Request</p>
          <ul>
            <li>SIT API document request (SIT)
              <div class="row">
                <div class="col-md-8 p-2 grey">  
                  <img src="../../assets/images/doc/new_sit.png" class="img-fluid mx-auto" alt="...">
                </div>
              </div>
            </li>
            <li>Monitoring status Production Request (request, revision, pending, rejected)
            <div class="row">
                <div class="col-md-8 p-2 grey">  
                  <img src="../../assets/images/doc/sit_list.png" class="img-fluid mx-auto" alt="...">
                </div>
              </div>
            </li>
          </ul>
          <p>&nbsp;</p>
          <p><br></p>
          
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
        </Widget>
      </div>
    </b-row>
  </div>
</template>

<script>
import axios from 'axios'
import backend from '@/server'
import Widget from '@/components/Widget/Widget';

export default {
  name: 'Documentations',
  components: {
    Widget
  },
  data() {
    return {
      model: {
      },
      loading: '',
      user_response: {},
      response_error: '',
    };
  },
  created() {
    this.load();
  },
  methods: {
    load() {
      // this.post_users();
    },
    async post_users() {
      var url = backend.backendURI + '/api/v1/user'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.post(url, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.users_response = resp.data
        this.response_error = 'User Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
      }
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
  },
  computed: {
  }
};
</script>

<style src="./Documentations.scss" lang="scss" />

