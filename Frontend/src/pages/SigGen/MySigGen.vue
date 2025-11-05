<template>
  <div class="mysiggen-page">
    <h2 class="page-title">Signature Generator - <span class="fw-semi-bold">OpenAPI</span></h2>
    <b-row>
      <b-col>
        <Widget
          title="<h5>Signature <span class='fw-semi-bold'>Generator</span></h5>"
          customHeader close collapse
        >
          <form ref="form" @submit.stop.prevent="handleSubmitnewApps">
            <b-form-group
              label="API Version"
              label-for="version-input"
              invalid-feedback="Version is required"
              :state="model.versionState"
              >
              <b-form-select
                id="version-input"
                v-model="model.version"
                @change="getSelectedProducts"
                :state="model.versionState"
                :options="versionOptions"
              ></b-form-select>
            </b-form-group>
            <b-form-group
              label="API Type"
              label-for="type-input"
              invalid-feedback="Type is required"
              :state="model.sigtypeState"
              >
              <b-form-select
                id="type-input"
                v-model="model.sigtype"
                @change="getSelectedProducts"
                :state="model.sigtypeState"
                :options="sigtypeOptions"
              ></b-form-select>
            </b-form-group>
            <b-form-group
              v-if="model.sigtype !== 'authorization'"
              label="Method"
              label-for="method-input"
              invalid-feedback="Method is required"
              :state="model.methodState"
              >
              <b-form-select
                id="method-input"
                v-model="model.method"
                @change="getSelectedProducts"
                :state="model.methodState"
                :options="methodOptions"
              ></b-form-select>
            </b-form-group>
            <b-form-group
              v-if="model.sigtype !== 'authorization'"
              label="URL Path"
              label-for="urlPath-input"
              invalid-feedback="URL Path is required"
              :state="model.urlPathState"
              >
              <b-form-select
                id="urlPath-input"
                v-model="model.urlPath"
                :state="model.urlPathState"
                :options="model.urlPathOptions"
              ></b-form-select>
            </b-form-group>
            <b-form-group
              label="Timestamp"
              label-for="timestamp-input"
              invalid-feedback="Timestamp is required"
              :state="model.timestampState"
            >
              <b-form-input
                id="timestamp-input"
                v-model="model.timestamp"
                :state="model.timestampState"
                required
              ></b-form-input>
            </b-form-group>
            <b-form-group
              label="ClientId"
              label-for="clientid-input"
              invalid-feedback="ClientId is required"
              :state="model.clientIdState"
            >
              <b-form-input
                id="clientid-input"
                v-model="model.clientId"
                :state="model.clientIdState"
                required
              ></b-form-input>
            </b-form-group>
            <b-form-group
              v-if="model.sigtype !== 'authorization'"
              label="ClientSecret"
              label-for="secret-input"
              invalid-feedback="Client Secret is required"
              :state="model.clientSecretState"
            >
              <b-form-input
                id="clientsecret-input"
                v-model="model.clientSecret"
                :state="model.clientSecretState"
                required
              ></b-form-input>
            </b-form-group>
            <b-form-group
              v-if="model.sigtype !== 'authorization'"
              label="Body"
              label-for="body-input"
              invalid-feedback="Body is required"
              :state="model.bodyState"
            >
              <b-form-textarea
                id="method-input"
                v-model="model.body"
                :state="model.bodyState"
                required
                rows="3"
                max-rows="6"
              ></b-form-textarea>
            </b-form-group>
            <b-form-group
              v-if="model.sigtype !== 'authorization'"
              label="Access Token"
              label-for="token-input"
              invalid-feedback="Access Token is required"
              :state="model.tokenState"
            >
              <b-form-textarea
                id="token-input"
                v-model="model.token"
                :state="model.tokenState"
                required
                rows="3"
                max-rows="6"
              ></b-form-textarea>
            </b-form-group>
          </form>
          <div class="clearfix">
            <div class="float-right">
              <b-button variant="default" class="mr-3" size="sm" @click="genSignature">Generate</b-button>
            </div>
            <p><p>Signature Generator</p></p>
          </div>
        </Widget>
        <Widget
          title="<h5>Signature <span class='fw-semi-bold'>Result</span></h5>"
          customHeader close collapse
        >
          <b-form-textarea
            id="token-input"
            v-model="model.signature"
            :state="model.signatureState"
            required
            rows="3"
            max-rows="6"
          ></b-form-textarea>
        </Widget>
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
          @ok="handleOKnotifResponse"
        >
          <p class="my-4">Response from server: {{ response_error }}</p>
        </b-modal>
      </b-col>
    </b-row>
  </div>
  
</template>

<script>
import axios from 'axios'
import Widget from '@/components/Widget/Widget';
import backend from '@/server'

export default {
  name: 'mysiggen',
  components: {
    Widget
  },
  data() {
    return {
      model: {
        version: '',
        sigtype: '',
        type: backend.serverType,
        method: '',
        urlPath: '',
        clientId: '',
        clientSecret: '',
        body: '',
        timestamp: '',
        accessToken : '',
        signature: '',
        versionState: null,
        sigtypeState: null,
        methodState: null,
        urlPathState: null,
        clientIdState: null,
        clientSecretState: null,
        bodyState: null,
        timestampState: null,
        isactiveState: null,
        productsOptions: [],
        urlPathOptions: [],
        accessTokenState: null,
        signatureSate: null
      },
      sigtypeOptions: [
        { value: 'authorization', text: 'Authorization', selected: true },
        { value: 'transaction', text: 'Transaction' },
      ],
      versionOptions: [
        { value: '1.0', text: 'V1.0', selected: true },
        { value: '2.0', text: 'V2.0' },
      ],
      methodOptions: [
        { value: 'POST', text: 'POST', selected: true },
        { value: 'GET', text: 'GET' },
        { value: 'PUT', text: 'PUT' },
      ],
      products_response: {},
      products_response_error: {},
      isLoading: false,
      isLoadingProducts: false,
      isLoadingSignature: false,
      signature_request_response: {},
      gen_response: {},
      response_error: '',
      selectedUser: {},
    }
  },
  created() {
    this.model.sigtype == "authorization"
    this.load()
  },
  methods: {
    load() {
      this.getProducts();
      var currentdate = new Date(); 
      this.model.timestamp = currentdate.getFullYear() + "-"
                + (currentdate.getMonth()+1)  + "-" 
                + currentdate.getDate() + "T"  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds() + ".000TZD";
    },
    getSelectedProducts() {
      this.model.urlPathOptions = []
      if (this.model.sigtype != "authorization") {
        for (let i = 0; i < this.model.productsOptions.length; i++) {
          if (this.model.productsOptions[i].version === this.model.version) {
            this.model.urlPathOptions.push({ value: this.model.productsOptions[i].value, text: this.model.productsOptions[i].text})
          }
        }
      }
    },
    async getProducts() {
      var url = backend.backendURI + '/api/v1/products/all?order_type=ASC&limit=100&page=1'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.get(url, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
          }
        );
        this.products_response = resp.data
        for (let i = 0; i < this.products_response.data.length; i++) {
          if (this.products_response.data[i].type === this.model.type) {
            this.model.productsOptions.push({ value: this.products_response.data[i].uripath, text: this.products_response.data[i].uripath, version: this.products_response.data[i].version})
          }
        }
        this.isLoadingProducts = true
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingProducts = true
      } finally {
        this.isLoadingProducts = true;
      }
    },
    async genAuthSignature() {
      this.isLoadingSignatureRequest = false;
      var url = backend.apinodeURI + '/api/v1.0/utilities/signature-auth'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.post(url, {
                "version":this.model.version,
                "clientId": this.model.clientId,
                "xTimestamp": this.model.timestamp
            },{
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token,
            }}
        );
        this.signature_request_response = resp.data
        this.model.signature = this.signature_request_response.signature
        this.response_error = 'Request Signature Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingSignatureRequest = true;
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingSignatureRequest = true;
      } finally {
        this.isLoadingSignatureRequest = true;
      }
    },
    async genTrxSignature() {
      this.isLoadingSignatureRequest = false;
      var url = backend.apinodeURI + '/api/v1.0/utilities/signature-service'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.post(url, {
                "version":this.model.version,
                "method":this.model.method,
                "urlPath":this.model.urlPath,
                "accessToken":this.model.accessToken,
                "body":this.model.body,
                "xTimestamp": this.model.timestamp,
                "clientId": this.model.clientId,
                "clientSecret": this.model.clientSecret
            },{
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token,
            }}
        );
        this.signature_request_response = resp.data
        this.model.signature = this.signature_request_response.signature
        this.response_error = 'Request Signature Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingSignatureRequest = true;
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingSignatureRequest = true;
      } finally {
        this.isLoadingSignatureRequest = true;
      }
    },
    genSignature(){
      this.model.signature = ''
      if (this.model.sigtype == 'authorization') {
        this.genAuthSignature()
      } else {
        if (this.model.version !== '') {
          this.genTrxSignature()
        } else {
          this.response_error = 'Deny Request, unknown version '
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
      }
    },
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity()
      this.model.versionState = valid,
      this.model.sigtypeState = valid
      this.model.methodState = valid
      this.model.urlPathState = valid
      this.model.clientIdState = valid
      this.model.clientSecretState = valid
      this.model.bodyState = valid
      this.model.timestampState = valid
      this.model.accessTokenState = valid
      this.model.signatureState = valid
      return valid
    },
    resetModal() {
      this.model.version = ''
      this.model.sigtype = ''
      this.model.method = ''
      this.model.urlPath = ''
      this.model.clientId = ''
      this.model.clientSecret = ''
      this.model.body = ''
      this.model.timestamp = ''
      this.model.accessToken = ''
      this.model.signature = ''
      this.model.versionState = null
      this.model.typeState = null
      this.model.methodState = null
      this.model.urlPathState = null
      this.model.clientIdState = null
      this.model.clientSecretState = null
      this.model.bodyState = null
      this.model.timestampState = null
      this.model.accessTokenState = null
      this.model.signatureState = null
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

<style src="./SigGen.scss" lang="scss" />
