<template>
  <div class="productions-page">
    <h2 class="page-title">SIT - Request - <span class="fw-semi-bold">OpenAPI</span></h2>
    <b-row>
      <b-col>
        <Widget
          title="<h5>Production Request <span class='fw-semi-bold'>List</span></h5>"
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
                  <th class="hidden-sm-down">Owner</th>
                  <th class="hidden-sm-down">Requested</th>
                  <th class="hidden-sm-down">Document</th>
                  <th class="hidden-sm-down">Approved</th>
                  <th class="hidden-sm-down">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in production_request_all_response" :key="row.user.username">
                  <td>
                    {{row.user.company}}
                    <br>
                    <b-badge variant="info" v-b-modal.profileInfo @click="profileUser(index)"><small>detail</small></b-badge>
                  </td>
                  <td>
                    <p class="mb-0">
                      <small>
                        <span class="fw-semi-bold">By:</span>
                        <span class="text-muted">&nbsp; {{row.requested_by}}</span>
                      </small>
                    </p>
                    <p>
                      <small>
                        <span class="fw-semi-bold">Type:</span>
                        <span class="text-muted">&nbsp; {{row.request_type}}</span>
                      </small>
                    </p>
                  </td>
                  <td>
                    <p class="mb-0">
                      <small>
                        <span class="fw-semi-bold">Template:</span>
                        <div v-if="row.template_file.length > 0">
                          <div v-for="rfile in getFiles(row.template_file)">
                            <span class="text-muted" >&nbsp; <a :href="getDocUrl(rfile)">{{getDocUrl(rfile)}}</a></span>
                          </div>
                        </div>
                        <br>
                        <b-badge variant="primary" v-b-modal.addTemplateFile @click="profileUser(index)"><small>add template</small></b-badge>
                      </small>
                    </p>
                    <p>
                      <small>
                        <span class="fw-semi-bold">Final File:</span>
                        <div v-if="row.final_file.length > 0">
                          <div v-for="rfile in getFiles(row.final_file)">
                            <span class="text-muted" >&nbsp; <a :href="getDocUrl(rfile)">{{getDocUrl(rfile)}}</a></span>
                          </div>
                        </div>
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
                    <b-badge variant="primary" v-b-modal.changeStatus @click="profileUser(index)"><small>{{getStatusValue(row.status)[1]}}</small></b-badge>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="clearfix">
            <div class="float-right">
              <b-button variant="default" class="mr-3" size="sm" v-b-modal.newProductionRequest>New</b-button>
            </div>
            <p><p>Productions Request</p></p>
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
            id="addTemplateFile"
            ref="modal"
            title="Add TemplateFile Production Request"
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKaddTemplateFile"
          >
            <form ref="form" @submit.stop.prevent="handleSubmitaddTemplateFile">
              <b-form-group
                label="Template File"
                label-for="templatefile-input"
                invalid-feedback="Template file is required"
                :state="model.templatefileState"
              >
                <b-button variant="info" size="sm" class="mb-2 mr-2 mt-3" @click="uploadDocumentFile">upload</b-button>
                <span class="input-group-btn">
                  <b-form-file
                    id="templatefile-input"
                    v-model="model.ftemplatefile"
                    :state="Boolean(model.templatefile)"
                    accept=".doc, .docx, .xls, .xlsx"
                    placeholder="Choose a file or drop it here..."
                    drop-placeholder="Drop file here..."
                    ref="file-templatedoc"
                  ></b-form-file>
                </span>
              </b-form-group>
            </form>
            <div v-if="!uploadReady" class="row justify-content-center align-items-center position-relative">
              <div v-if="this.model.docurl != ''" class="col-md-12"><a :href="getDocUrl(this.model.docurl)">Click Here to Open Document</a></div>
              <div v-else class="col-md-12"><span class="fw-semi-bold">None File</span></div>
            </div>
            <div v-else class="row justify-content-center align-items-center position-relative">
              <i class="fa fa-spinner fa-spin fa-3x fa-fw"></i>
            </div>
          </b-modal>  
          <b-modal
            id="changeStatus"
            ref="modal"
            title="Production Request Change Status"
            scrollable
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKchangeStatus"
          >
            <form ref="form" @submit.stop.prevent="handleSubmitchangeStatus">
              <b-form-group
                label="Status"
                label-for="status-input"
                invalid-feedback="Status is required"
                :state="model.statusState"
                >
                <b-form-select
                  id="status-input"
                  v-model="model.status"
                  :state="model.statusState"
                  :options="statusOptions"
                ></b-form-select>
              </b-form-group>
            </form>
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
            id="newProductionRequest"
            ref="modal"
            title="Create New Production Request"
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKnewProductionRequest"
          >
            <form ref="form" @submit.stop.prevent="handleSubmitnewProductionRequest">
              <b-form-group
                label="User"
                label-for="user-input"
                invalid-feedback="User is required"
                :state="model.userIdState"
                >
                <b-form-select
                  id="user-input"
                  v-model="model.userId"
                  :state="model.userIdState"
                  :options="model.userOptions"
                ></b-form-select>
              </b-form-group>
              <b-form-group
                label="RequestedBy"
                label-for="requestedby-input"
                invalid-feedback="RequestedBy is required"
                :state="model.requestedbyState"
              >
                <b-form-input
                  id="requestedby-input"
                  v-model="model.requestedby"
                  :state="model.requestedbyState"
                  required
                ></b-form-input>
              </b-form-group>
              <b-form-group
                label="Type"
                label-for="requesttype-input"
                invalid-feedback="Requested Type is required"
                :state="model.requesttypeState"
                >
                <b-form-select
                  id="type-input"
                  v-model="model.requesttype"
                  :state="model.requesttypeState"
                  :options="typeOptions"
                ></b-form-select>
              </b-form-group>
              <b-form-group
                label="TemplateFile"
                label-for="templatefile-input"
                invalid-feedback="Template file is required"
                :state="model.templatefileState"
              >
                <b-button variant="info" size="sm" class="mb-2 mr-2 mt-3" @click="uploadDocumentFile">upload</b-button>
                <span class="input-group-btn">
                  <b-form-file
                    id="templatefile-input"
                    v-model="model.templatefile"
                    :state="Boolean(model.templatefile)"
                    accept=".doc, .docx, .xls, .xlsx"
                    placeholder="Choose a file or drop it here..."
                    drop-placeholder="Drop file here..."
                    ref="file-templatedoc"
                  ></b-form-file>
                </span>
              </b-form-group>
            </form>
            <div v-if="!uploadReady" class="row justify-content-center align-items-center position-relative">
              <div v-if="this.model.docurl != ''" class="col-md-12"><a :href="getDocUrl(this.model.docurl)">Click Here to Open Document</a></div>
              <div v-else class="col-md-12"><span class="fw-semi-bold">None File</span></div>
            </div>
            <div v-else class="row justify-content-center align-items-center position-relative">
              <i class="fa fa-spinner fa-spin fa-3x fa-fw"></i>
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
  name: 'productions-page',
  components: {
    Widget
  },
  data() {
    return {
      model: {
        userid:'',
        requestedby:'',
        requesttype:'',
        status: '',
        templatefile:'',
        templatesfile:[],
        finalfile:'',
        finalsfile:[],
        approvedat:'',
        approvedby:'',
        userOptions: [],
        requestedbyState: null,
        requesttypeState: null,
        statusState: null,
        templatefileState: null,
        finalfileState: null,
        approvedatState: null,
        approvedbyState: null,
        templateurl: '',
        docurl:''
      },
      statusOptions: [
          { value: '10-Requested', text: 'Requested' },
          { value: '20-AggreementReviewed', text: 'Aggreement Reviewed' },
          { value: '30-AggreementCompleted', text: 'Aggreement Completed' },
          { value: '40-SITRequested', text: 'SIT Requested' },
          { value: '50-SITReviewed', text: 'SIT Reviewed' },
          { value: '60-SIT Revision', text: 'SIT Revision' },
          { value: '70-SIT Completed', text: 'SIT Completed' },
          { value: '80-Rejected', text: 'Rejected' },
          { value: '90-Cancelled', text: 'Cancelled' },
          { value: '100-Accepted', text: 'Accepted' },
      ],
      typeOptions: [
          { value: 'production', text: 'Production' },
      ],
      showPreview: false,
      docPreview:'',
      docUploadError: '',
      uploadingDoc: false,
      loadingUpload: false,
      imagePreview: '',
      isLoading: false,
      isLoadingProductionRequest: false,
      selectedUser: {},
      users_response: [],
      production_request_response: {},
      production_request_all_response: [],
      response_error: '',
      upload_response: {},
      upload_response_error: {},
      apiresult: '',
    };
  },
  created() {
    this.load();
  },
  methods: {
    load() {
      this.getUsers();
      this.getProductionRequest();
    },
    getStatusValue(value) {
      return value.split('-')
    },
    getDocUrl(path) {
      return backend.minioURI + path
    },
    getFiles(value) {
      return value.split(',')
    },
    profileUser(index) {
      this.selectedUser = this.production_request_all_response[index];
    },
    async updateChangeStatus(status) {
      this.isLoadingProductionRequest = false;
      var url = backend.backendURI + '/api/v1/production/status?production_status=' + status + '&db_id=' + this.selectedUser.db_id 
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.put(url, {
        params: {
          "status": status,
        }}, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.production_request_response = resp.data.data
        this.response_error = 'Change Status Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingProductionRequest = true;
        this.getProductionRequest();
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingProductionRequest = true;
      } finally {
        this.isLoadingProductionRequest = true;
      }
    },
    async getProductionRequest() {
      this.isLoadingProductionRequest = false;
      var url = backend.backendURI + '/api/v1/production/all?order_type=ASC&limit=100&page=1'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.get(url, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.production_request_all_response = resp.data.data
        this.isLoadingProductionRequest = true;
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingProductionRequest = true;
      } finally {
        this.isLoadingProductionRequest = true;
      }
    },
    async createNewProductionRequest() {
      this.isLoadingProductionRequest = false;
      var url = backend.backendURI + '/api/v1/production'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.post(url, {
                "user_id" : this.model.userId,
                "requested_by" : this.model.requestedby,
                "request_type" : this.model.requesttype,
                "status" : "10,Requested",
                "template_file" : this.model.docurl,
                "final_file" : "",
                "approved_at" : "1970-01-01 00:00:00",
                "approved_by" : "",
                "isactive": true
            },{
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token,
            }}
        );
        this.production_request_response = resp.data
        this.response_error = 'Request SIT Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingProductionRequest = true;
        this.getProductionRequest();
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingProductionRequest = true;
      } finally {
        this.isLoadingProductionRequest = true;
      }
    },
    async addTemplatFile(templatefile) {
      this.isLoadingProductionRequest = false;
      var url = backend.backendURI + '/api/v1/production/templatefile?templatefile=' + templatefile  + '&db_id=' + this.selectedUser.db_id 
      var token = window.localStorage.getItem('openapi-token')
      var tmpfiles = this.getFiles(this.selectedUser.template_file)
      var resultfiles = '';
      for (let i = 0; i < tmpfiles.length; i++) {
          resultfiles = resultfiles + tmpfiles[i] + ','
      }
      resultfiles = resultfiles + templatefile
      try {
        const resp = await axios.put(url, {
        params: {
          "template_file": resultfiles,
        }}, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.production_request_response = resp.data.data
        this.response_error = 'Template Document Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingProductionRequest = true;
        this.getProductionRequest();
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingProductionRequest = true;
      } finally {
        this.isLoadingProductionRequest = true;
      }
    },
    async addFinalFile(finalfile) {
      this.isLoadingProductionRequest = false;
      var url = backend.backendURI + '/api/v1/production/finalfile?finalfile=' + finalfile  + '&db_id=' + this.selectedUser.db_id 
      var token = window.localStorage.getItem('openapi-token')
      tmpfiles = this.getFiles(this.selectedUser.final_file)
      resultfiles = '';
      for (let i = 0; i < tmpfiles.length; i++) {
          resultfiles = resultfiles + tmpfiles[i] + ','
      }
      resultfiles = resultfiles + finalfile
      try {
        const resp = await axios.put(url, {
        params: {
          "final_file": resultfiles,
        }}, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.production_request_response = resp.data.data
        this.response_error = 'Upload Document Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingProductionRequest = true;
        this.getProductionRequest();
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingProductionRequest = true;
      } finally {
        this.isLoadingProductionRequest = true;
      }
    },
    async getUsers() {
      var url = backend.backendURI + '/api/v1/user/all?order_type=ASC&limit=100&page=1'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.get(url, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.users_response = resp.data
        for (let i = 0; i < this.users_response.data.length; i++) {
          this.model.userOptions.push({ value: this.users_response.data[i].user_id, text: this.users_response.data[i].username})
        }
        this.isLoadingUser = true
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingUser = true
      } finally {
        this.isLoadingUser = true;
      }
    },
    uploadDocumentFile(){
      this.showPreview = false;
      this.file = this.$refs['file-templatedoc'].files[0];
      let reader  = new FileReader();
      if( this.file ){
        if ( /\.(docx|pdf)$/i.test( this.file.name ) ) {
          reader.readAsDataURL( this.file );
        }
        if (this.file.size > 1000000) {
          this.apiresult = "Forbidden, File size more than 1 MByte"
          return
        }
      }
      reader.addEventListener("load", function () {
        let formData = new FormData();
        formData.append('file', this.file);
        this.putDocFile(formData);

        this.showPreview = true;
        this.docPreview = reader.result;
      }.bind(this), false);
    },
    async putDocFile(docData) {
      this.loadingUpload = true;
      this.uploadingDoc = false
      this.docUploadError = "";
      var url = backend.backendURI + '/api/v1/upload/document'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.post(url, docData, {
          headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'multipart/form-data',
            }}
        );
        this.upload_response = resp.data
        this.model.docurl = this.upload_response.data.url
        this.response_error = 'Upload Document Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.loadingUpload = false;
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.loadingUpload = false;
      }    
    },
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity()
      this.model.requestedbyState  = valid
      this.model.requesttypeState  = valid
      this.model.statusState  = valid
      this.model.templatefileState  = valid
      this.model.finalfileState  = valid
      this.model.approvedatState  = valid
      this.model.approvedbyState  = valid
      return valid
    },
    resetModal() {
      this.model.userid = ''
      this.model.requestedby = ''
      this.model.requesttype = ''
      this.model.status = ''
      this.model.templatefile = ''
      this.model.finalfile = ''
      this.model.approvedat = ''
      this.model.approvedby = ''
      this.model.docurl = ''
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
    handleOKnewProductionRequest(bvModalEvt) {
      this.loadingUpload = true
      bvModalEvt.preventDefault();
      this.handleSubmitnewProductionRequest();
    },
    handleSubmitnewProductionRequest() {
      if (!this.checkFormValidity()) {
        return
      }
      this.$nextTick(() => {
        this.createNewProductionRequest();
        this.$bvModal.hide('newProductionRequest');
      })
    },
    handleOKchangeStatus(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmitchangeStatus();
    },
    handleSubmitchangeStatus() {
      if (!this.checkFormValidity()) {
        return
      }
      this.$nextTick(() => {
        this.updateChangeStatus(this.model.status)
        this.$bvModal.hide('changeStatus')
      })
    },
    handleOKaddTemplateFile(bvModalEvt) {
      this.loadingUpload = true
      bvModalEvt.preventDefault();
      this.handleSubmitaddTemplateFile();
    },
    handleSubmitaddTemplateFile() {
      if (!this.checkFormValidity()) {
        return
      }
      this.$nextTick(() => {
        this.addTemplatFile(this.model.docurl)
        this.$bvModal.hide('addTemplateFile')
      })
    },
    handleOKaddFinalFile(bvModalEvt) {
      this.loadingUpload = true
      bvModalEvt.preventDefault(this.model.finalfile);
      this.handleSubmitaddFinalFile();
    },
    handleSubmitaddFinalFile() {
      if (!this.checkFormValidity()) {
        return
      }
      this.$nextTick(() => {
        this.addFinalFile(this.model.docurl)
        this.$bvModal.hide('addFinalFile')
      })
    },
  },
  computed: {
    dataReady() {
      return this.isLoadingProductionRequest
    },
    uploadReady() {
      return this.loadingUpload && this.showPreview
    }
  }
};
</script>

<style src="./Productions.scss" lang="scss" />
