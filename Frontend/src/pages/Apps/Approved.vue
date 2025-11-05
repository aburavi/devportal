<template>
  <div class="approved-page">
    <h2 class="page-title">Apps Approval - <span class="fw-semi-bold">OpenAPI</span></h2>
    <b-row>
      <b-col>
        <Widget
          title="<h5>Apps <span class='fw-semi-bold'>List</span></h5>"
          customHeader close collapse
        >
          <div class="table-resposive">
          
            <b-skeleton-table v-if="!dataReady"
              :rows="3"
              :columns="4"
              :table-props="{ bordered: true, striped: true }"
              :loading="dataReady"
            ></b-skeleton-table>
              <table v-else  class="table">
                <thead>
                  <tr>
                    <th>Owner</th>
                    <th>Apps Name</th>
                    <th>Consumer_key</th>
                    <th>Consumer_secret</th>
                    <th class="hidden-sm-down">Type</th>
                    <th class="hidden-sm-down">Product</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, index) in apps_response" :key="row.db_id">
                    <td>
                      {{row.user.company}}
                      <br>
                      <b-badge variant="info" v-b-modal.profileInfo @click="profileUser(index)"><small>detail</small></b-badge>
                    </td>
                    <td>
                      {{row.name}}
                      <br>
                      <b-badge variant="warning" v-b-modal.approvedApps @click="profileUser(index)"><small>Waiting Approval</small></b-badge>
                    </td>
                    <td class="text-semi-muted">
                       {{row.consumer_key}}
                    </td>
                    <td class="text-semi-muted">
                      {{row.consumer_secret}}
                    </td>
                    <td>
                      {{row.type}}
                    </td>
                    <td class="text-semi-muted">
                      <tr v-for="prod in row.products">
                          <small>{{prod}}</small>
                      </tr>
                    </td>
                  </tr>
                </tbody>
              </table>
          </div>
          <div class="clearfix">
            <p><p>Apps Registration Approval</p></p>
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
            id="profileInfo"
            ref="modal"
            title="Profile Info"
            scrollable
            ok-only
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKprofileInfo"
          >
            <div v-if="Object.keys(selectedUser).length !== 0">
              <div class="widget-top-overlay widget-padding-md clearfix bg-info text-white">
                <div class="row mt-2">
                  <div class="col-md-6"><label class="labels">Name</label><input type="text" class="form-control" :value="selectedUser.user.firstname" readonly></div>
                  <div class="col-md-6"><label class="labels">Surname</label><input type="text" class="form-control" :value="selectedUser.user.lastname" readonly></div>
                </div>
                <div class="row mt-3">
                  <div class="col-md-12"><label class="labels">Email</label><input type="text" class="form-control" :value="selectedUser.user.email" readonly></div>
                  <div class="col-md-12"><label class="labels">Phone</label><input type="text" class="form-control" :value="selectedUser.user.phone" readonly></div>
                  <div class="col-md-12"><label class="labels">Company</label><input type="text" class="form-control" :value="selectedUser.user.company" readonly></div>
                  <div class="col-md-12"><label class="labels">Address</label><input type="text" class="form-control" :value="selectedUser.user.address" readonly></div>
                </div>
              </dev>
            </div>
          </b-modal>

          <b-modal
            id="approvedApps"
            ref="modal"
            title="Approved New Apps"
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKapprovedApps"
          >
            <form ref="form" @submit.stop.prevent="handleSubmitapprovedApps">
              <b-form-group
                label="Source Account"
                label-for="srcAccount-input"
                invalid-feedback="Source Account is required"
                :state="model.srcAccountState"
              >
                <b-form-input
                  id="srcAccount-input"
                  v-model="model.srcAccount"
                  :state="model.srcAccountState"
                  required
                ></b-form-input>
              </b-form-group>

              <b-form-group
                label="Max Hit Rate"
                label-for="max-input"
                invalid-feedback="Max Hit Rate is required"
                :state="model.maxState"
              >
                <b-form-select
                  id="max-input"
                  v-model="model.max"
                  :state="model.maxState"
                  :options="maxRateOptions"
                ></b-form-select>
              </b-form-group>

              <b-form-group
                label="isActive"
                label-for="isactive-input"
                invalid-feedback="isActive is required"
                :state="model.isactiveState"
              >
                <b-form-select
                  id="isactive-input"
                  v-model="model.isactive"
                  :state="model.isactiveState"
                  :options="isActiveOptions"
                ></b-form-select>
              </b-form-group>
            </form>
          </b-modal>

        </Widget>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import axios from 'axios'
import Widget from '@/components/Widget/Widget';
import backend from '@/server'

export default {
  name: 'Approved',
  components: {
    Widget
  },
  data() {
    return {
      model: {
        name: '',
        dbId: '',
        type: backend.serverType,
        srcAccount: '',
        max: '',
        isactive: true,
        nameState: null,
        dbIdState: null,
        consumerKeyState: null,
        typeState: null,
        srcAccountState: null,
        isactiveState: null,
        maxState: null,
      },
      isActiveOptions: [
          { value: 'true', text: 'True' },
          { value: 'false', text: 'False' },
      ],
      maxRateOptions: [
          { value: 30, text: '30 hit/minutes' },
          { value: 60, text: '60 hit/minutes' },
          { value: 90, text: '90 hit/minutes' },
          { value: 120, text: '120 hit/minutes' },
      ],
      isLoading: false,
      isLoadingApps: false,
      apps_response: [],
      response_error: '',
      new_apps_response: {},
      new_apps_response_error: {},
      selectedUser: {},
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      this.getApps();
    },
    profileUser(index) {
      this.selectedUser = this.apps_response[index];
    },
    async getApps() {
      var url = backend.backendURI + '/api/v1/approved/all?order_type=ASC&limit=100&page=1'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.get(url, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.apps_response = resp.data.data
        this.isLoading = true
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoading = true
      } finally {
        this.isLoading = true;
      }
    },
    async approvedNewApps() {
      this.isLoading = false
      var url = backend.backendURI + '/api/v1/approved/apps'
      var token = window.localStorage.getItem('openapi-token')
      var data = {
        "consumer_key": this.selectedUser.consumer_key,
        "consumer_secret": this.selectedUser.consumer_secret,
        "name": this.selectedUser.consumer_key,
        "src_accounts": this.model.srcAccount,
        "max_rate":  this.model.max,
        "isactive": this.model.isactive,
      }
      try {
        const resp = await axios.post(url, data , {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }}
        );
        this.new_apps_response = resp.data
        this.response_error = 'Approved Apps Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.getApps()
        this.isLoadingApps = true
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingApps = true
      } finally {
        this.isLoadingApps = true;
      }
    },
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity()
      this.model.nameState  = valid
      this.model.typeState  = valid
      this.model.srcAccountState  = valid
      this.model.isactiveState  = valid
      return valid
    },
    resetModal() {
      this.model.dbId = ''
      this.model.name = ''
      this.model.srcAccount = ''
      this.model.isactive = true,
      this.model.dbIdState = null
      this.model.nameState = null
      this.model.srcAccountState = null
      this.model.isactiveState = null
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
    handleOKprofileInfo(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmitprofileInfo();
    },
    handleSubmitprofileInfo() {
      this.$nextTick(() => {
        this.$bvModal.hide('profileInfo');
      })
    },
    handleOKapprovedApps(bvModalEvt) {
      bvModalEvt.preventDefault()
      this.handleSubmitapprovedApps()
    },
    handleSubmitapprovedApps() {
      if (!this.checkFormValidity()) {
        return
      }
      this.$nextTick(() => {
        this.approvedNewApps()
        this.$bvModal.hide('approvedApps')
      })
    },
  },
  computed: {
    dataReady() {
      return this.isLoading
    }
  },
};
</script>

<style src="./Apps.scss" lang="scss" />
