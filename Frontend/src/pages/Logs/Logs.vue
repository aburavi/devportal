<template>
  <div class="logs-page">
    <h2 class="page-title">Logs - SIT - Request - <span class="fw-semi-bold">OpenAPI</span></h2>
    <b-row>
      <b-col>
        <Widget
          title="<h5>Log Production Request <span class='fw-semi-bold'>List</span></h5>"
          customHeader close collapse
        >
          <div class="table-resposive">
            <b-skeleton-table v-if="!dataReady"
              :rows="3"
              :columns="4"
              :table-props="{ bordered: true, striped: true }"
              :loading="dataReady"
            >
            </b-skeleton-table>
            <table v-else class="table">
              <thead>
                <tr>
                  <th class="hidden-sm-down">Date</th>
                  <th class="hidden-sm-down">Owner</th>
                  <th class="hidden-sm-down">Content</th>
                  <th class="hidden-sm-down">Description</th>
                  <th class="hidden-sm-down">Approved</th>
                  <th class="hidden-sm-down">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in log_production_request_response" :key="row.user.username">
                  <td>
                    <p class="mb-0">
                      <small>
                        <span class="text-muted">&nbsp; {{row.created_at}}</span>
                      </small>
                    </p>
                  </td>
                  <td>
                    {{row.user.company}}
                    <br>
                    <b-badge variant="info" v-b-modal.profileInfo @click="profileUser(index)"><small>detail</small></b-badge>
                  </td>
                  <td>
                    <p class="mb-0">
                      <small>
                        <span class="text-muted">&nbsp; {{row.content}}</span>
                      </small>
                    </p>
                    <p>
                      <small>
                        <span class="fw-semi-bold">Type:</span>
                        <span class="text-muted">&nbsp; {{row.content_type}}</span>
                      </small>
                    </p>
                  </td>
                  <td>
                    <p>
                      <small>
                        <span class="fw-semi-bold">Requested By:</span>
                        <span class="text-muted">&nbsp; {{getDescriptionValue(row.description)[0]}}</span>
                      </small>
                    </p>
                    <p>
                      <small>
                        <span class="fw-semi-bold">Type:</span>
                        <span class="text-muted">&nbsp; {{getDescriptionValue(row.description)[1]}}</span>
                      </small>
                    </p>
                    <p>
                      <small>
                        <span class="fw-semi-bold">Template File:</span>
                        <span class="text-muted">&nbsp; {{getDescriptionValue(row.description)[2]}}</span>
                      </small>
                    </p>
                    <p>
                      <small>
                        <span class="fw-semi-bold">Final File:</span>
                        <span class="text-muted">&nbsp; {{getDescriptionValue(row.description)[3]}}</span>
                      </small>
                    </p>
                  </td>
                  <td class="text-semi-muted">
                    <p class="mb-0">
                      <small>
                        <span class="fw-semi-bold">By:</span>
                        <span class="text-muted">&nbsp; {{row.approved_by}}</span>
                      </small>
                    </p>
                    <p>
                      <small>
                        <span class="fw-semi-bold">Date:</span>
                        <span class="text-muted">&nbsp; {{row.approved_at}}</span>
                      </small>
                    </p>
                  </td>
                  <td class="width-150">
                    <b-progress :variant="success" :value=getStatusValue(row.status)[0] :max="100" class="progress-sm mb-xs"/>
                    <br>
                    <b-badge variant="primary"><small>{{getStatusValue(row.status)[1]}}</small></b-badge>
                  </td>
                </tr>
              </tbody>
            </table>
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
        </Widget>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import axios from 'axios';
import backend from '@/server';
import Widget from '@/components/Widget/Widget';

export default {
  name: 'logs-page',
  components: {
    Widget
  },
  data() {
    return {
      model: {
        status: '',
        statusState: null,
      },
      isLoadingLogProductionRequest: false,
      log_production_request_response: [],
      response_error: {},
      selectedUser: {},
    }
  },
  created() {
    this.load();
  },
  methods: {
    load() {
      this.getLogProductionRequest();
    },
    getStatusValue(value) {
      return value.split('-')
    },
    getDescriptionValue(value) {
      return value.split(':')
    },
    profileUser(index) {
      this.selectedUser = this.log_production_request_response[index];
    },
    async getLogProductionRequest() {
      this.isLoadingProductionRequest = false;
      var url = backend.backendURI + '/api/v1/history/all?order_type=ASC&limit=100&page=1'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.get(url, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.log_production_request_response = resp.data.data
        this.isLoadingLogProductionRequest = true;
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingLogProductionRequest = true;
      } finally {
        this.isLoadingLogProductionRequest = true;
      }
    },
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity()
      this.model.statusState  = valid
      return valid
    },
    resetModal() {
      this.model.status = ''
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
  },
  computed: {
    dataReady() {
      return this.isLoadingLogProductionRequest
    },
  }
};
</script>

<style src="./Logs.scss" lang="scss" />
