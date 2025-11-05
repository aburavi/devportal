<template>
  <div class="myproductions-page">
    <h2 class="page-title">Productions Tenant Request - <span class="fw-semi-bold">OpenAPI</span></h2>
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
                  <th class="hidden-sm-down">Requested</th>
                  <th class="hidden-sm-down">Document</th>
                  <th class="hidden-sm-down">Approved</th>
                  <th class="hidden-sm-down">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in production_request_all_response" :key="row.db_id">
                  <td>
                    <p class="mb-0">
                      <small>
                        <span class="fw-semi-bold">By:</span>
                        <span class="text-muted">&nbsp; {{row.EntityProductionRequest.requested_by}}</span>
                      </small>
                    </p>
                    <p>
                      <small>
                        <span class="fw-semi-bold">Type:</span>
                        <span class="text-muted">&nbsp; {{row.EntityProductionRequest.request_type}}</span>
                      </small>
                    </p>
                  </td>
                  <td>
                    <p class="mb-0">
                      <small>
                        <span class="fw-semi-bold">Template:</span>
                        <div v-if="row.EntityProductionRequest.template_file.length !== 0">
                          <div v-for="rfile in getFiles(row.EntityProductionRequest.template_file)">
                            <span class="text-muted" >&nbsp; <a :href="getDocUrl(rfile)">{{getDocUrl(rfile)}}</a></span>
                          </div>
                        </div>
                      </small>
                    </p>
                    <p>
                      <small>
                        <span class="fw-semi-bold">Final File:</span>
                        <div v-if="row.EntityProductionRequest.final_file.length !== 0">
                          <div v-for="rfile in getFiles(row.EntityProductionRequest.final_file)">
                            <span class="text-muted" >&nbsp; <a :href="getDocUrl(rfile)">{{getDocUrl(rfile)}}</a></span>
                          </div>
                        </div>
                        <br>
                        <b-badge variant="primary" v-b-modal.addFinalFile @click="profileUser(index)"><small>add FinalFile</small></b-badge>
                      </small>
                    </p>
                  </td>
                  <td class="text-semi-muted">
                    <p class="mb-0">
                      <small>
                        <span class="fw-semi-bold">By:</span>
                        <span class="text-muted">&nbsp; {{row.EntityProductionRequest.approved_by}}</span>
                      </small>
                    </p>
                    <p>
                      <small>
                        <span class="fw-semi-bold">Date:</span>
                        <span class="text-muted">&nbsp; {{row.EntityProductionRequest.approved_at}}</span>
                      </small>
                    </p>
                  </td>
                  <td class="width-150">
                    <b-progress :variant="success" :value=getStatusValue(row.EntityProductionRequest.status)[0] :max="100" class="progress-sm mb-xs"/>
                    <br>
                    <b-badge variant="primary"><small>{{getStatusValue(row.EntityProductionRequest.status)[1]}}</small></b-badge>
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
            id="addFinalFile"
            ref="modal"
            title="Add FinalFile Production Request"
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKaddFinalFile"
          >
            <form ref="form" @submit.stop.prevent="handleSubmitaddFinalFile">
              <b-form-group
                label="Final File"
                label-for="finalfile-input"
                invalid-feedback="Final file is required"
                :state="model.finalfileState"
              >
                <b-button variant="info" size="sm" class="mb-2 mr-2 mt-3" @click="uploadDocumentFile">upload</b-button>
                <span class="input-group-btn">
                  <b-form-file
                    id="finalfile-input"
                    v-model="model.finalfile"
                    :state="Boolean(model.finalfile)"
                    accept=".doc, .docx, .xls, .xlsx"
                    placeholder="Choose a file or drop it here..."
                    drop-placeholder="Drop file here..."
                    ref="file-finaldoc"
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
            id="newProductionRequest"
            ref="modal"
            title="Create New Production Request"
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKnewProductionRequest"
          >
            <form ref="form" @submit.stop.prevent="handleSubmitnewProductionRequest">
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
                label="FinalFile"
                label-for="finalfile-input"
                invalid-feedback="Final file is required"
                :state="model.finalfileState"
              >
                <b-button variant="info" size="sm" class="mb-2 mr-2 mt-3" @click="uploadDocumentFile">upload</b-button>
                <span class="input-group-btn">
                  <b-form-file
                    id="finalfile-input"
                    v-model="model.finalfile"
                    :state="Boolean(model.finalfile)"
                    accept=".doc, .docx, .xls, .xlsx"
                    placeholder="Choose a file or drop it here..."
                    drop-placeholder="Drop file here..."
                    ref="file-finaldoc"
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
import jwt_decode from 'jwt-decode'

export default {
  name: 'myproductions-page',
  components: {
    Widget
  },
  data() {
    return {
      model: {
        userId:'',
        requestedby:'',
        requesttype:'',
        status: '',
        templatefile:'',
        templatesfile:[],
        finalfile:'',
        approvedat:'',
        approvedby:'',
        requestedbyState: null,
        requesttypeState: null,
        statusState: null,
        templatefileState: null,
        finalfileState: null,
        approvedatState: null,
        approvedbyState: null,
        templateurl: '',
        docurl: '',
      },
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
      production_request_all_response: [],
      production_request_response: {},
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
      let token = window.localStorage.getItem('openapi-token')
      let decoded_token = jwt_decode(token);
      this.model.userId = decoded_token.sub
      this.getProductionRequest();
    },
    getStatusValue(value) {
      return value.split('-')
    },
    getDocUrl(path) {
      return backend.minioURI + path
    },
    getFiles(value) {
      return value?.split(',')
    },
    profileUser(index) {
      this.selectedUser = this.production_request_all_response[index];
    },
    async addFinalFile(finalfile) {
      this.isLoadingProductionRequest = false;
      var url = backend.backendURI + '/api/v1/production/finalfile?finalfile=' + finalfile  + '&db_id=' + this.selectedUser.db_id 
      var token = window.localStorage.getItem('openapi-token')
      var tmpfiles = this.getFiles(this.selectedUser.final_file)
      var resultfiles = '';
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
        this.production_request_response = err.response.data.remark
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
      var url = backend.backendURI + '/api/v1/production/user/' + this.model.userId
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
            "request_type" : "production",
            "status" : "10-Requested",
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
        this.production_request_response = err.response.data.remark
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
    uploadDocumentFile(){
      this.model.docurl='';
      this.showPreview = false;
      this.file = this.$refs['file-finaldoc'].files[0];
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
        this.response_error = 'Upload Document Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.model.docurl = this.upload_response.data.url
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
    handleOKaddFinalFile(bvModalEvt) {
      this.loadingUpload = true
      bvModalEvt.preventDefault();
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
        this.createnewProductionRequest();
        this.$bvModal.hide('newProductionRequest');
      })
    }
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
