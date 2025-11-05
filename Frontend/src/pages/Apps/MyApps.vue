<template>
  <div class="apps-page">
    <h2 class="page-title">Apps - <span class="fw-semi-bold">OpenAPI</span></h2>
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
                    <th>Apps Name</th>
                    <th>Consumer_key</th>
                    <th>Consumer_secret</th>
                    <th class="hidden-sm-down">AccountNo</th>
                    <th class="hidden-sm-down">Product</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in apps_response" :key="row.db_id">
                    <td>
                      {{row.EntityApps.name}}
                      <br>
                      <b-badge variant="info"><small>{{row.EntityApps.type}}</small></b-badge>
                    </td>
                    <td class="text-semi-muted">
                       {{row.EntityApps.consumer_key}}
                    </td>
                    <td class="text-semi-muted">
                      {{row.EntityApps.consumer_secret}}
                    </td>
                    <td class="text-semi-muted">
                      {{row.EntityApps.src_accounts[0]}}
                    </td>
                    <td class="text-semi-muted">
                      <tr v-for="prod in row.EntityApps.products">
                          <small>{{prod}}</small>
                      </tr>
                    </td>
                  </tr>
                </tbody>
              </table>
          </div>
          <div class="clearfix">
            <div class="float-right">
              <b-button variant="default" class="mr-3" size="sm" v-b-modal.newApps>New</b-button>
            </div>
            <p><p>Apps Registration</p></p>
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
            id="newApps"
            ref="modal"
            title="Create New Apps"
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKnewApps"
          >
            <form ref="form" @submit.stop.prevent="handleSubmitnewApps">
              <b-form-group
                label="Apps Name"
                label-for="name-input"
                invalid-feedback="Name of product required"
                :state="model.nameState"
              >
                <b-form-input
                  id="name-input"
                  v-model="model.name"
                  :state="model.nameState"
                  required
                ></b-form-input>
              </b-form-group>

              <b-form-group
                label="Products"
                label-for="products-input"
                invalid-feedback="Products is required"
                :state="model.productsState"
                >
                <b-form-checkbox-group
                  id="products-input"
                  v-model="model.products"
                  :state="model.productsState"
                  :options="model.productsOptions"
                ></b-form-checkbox-group>
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
import jwt_decode from 'jwt-decode'
import Widget from '@/components/Widget/Widget';
import backend from '@/server'

export default {
  name: 'Apps',
  components: {
    Widget
  },
  data() {
    return {
      model: {
        userId: '',
        name: '',
        consumerKey: '',
        consumerSecret: '',
        type: backend.serverType,
        srcAccount: '',
        products: [],
        isactive: true,
        userIdState: null,
        nameState: null,
        consumerKeyState: null,
        consumerSecretState: null,
        typeState: null,
        srcAccountState: null,
        productsState: null,
        isactiveState: null,
        userOptions: [],
        srcAccountOptions: [],
        productsOptions: [],
      },
      typeOptions: [
          { value: 'sandbox', text: 'Sandbox' },
      ],
      isActiveOptions: [
          { value: 'true', text: 'True' },
          { value: 'false', text: 'False' },
      ],
      isLoading: false,
      isLoadingUser: false,
      isLoadingApps: false,
      isLoadingProducts: false,
      apps_response: [],
      response_error: '',
      new_apps_response: {},
      new_apps_response_error: {},
      products_response: {},
      products_response_error: {},
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
      this.getApps();
      this.getProducts();
    },
    async getApps() {
      var url = backend.backendURI + '/api/v1/apps/user/' + this.model.userId
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
      }
    },
    async createNewApps() {
      var url = backend.backendURI + '/api/v1/apps'
      var token = window.localStorage.getItem('openapi-token')
      this.model.srcAccountOptions.push(this.model.srcAccount)
      var data = {
        "user_id": this.model.userId,
        "name": this.model.name + '-' + this.model.type,
        "consumer_key": "",
        "consumer_secret": "",
        "type": model.type,
        "src_accounts": [],
        "max_rate": "0",
        "products": this.model.products,
        "isactive": false,
      }
      try {
        const resp = await axios.post(url, data , {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }}
        );
        this.new_apps_response = resp.data
        this.isLoading = false
        this.response_error = 'Create Apps Success'
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
          if (this.response_error == '')
            this.response_error = 'Request Failed'
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingApps = true
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
            this.model.productsOptions.push({ value: this.products_response.data[i].uripath, text: this.products_response.data[i].name})
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
      }
    },
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity()
      this.model.userIdState  = valid
      this.model.nameState  = valid
      this.model.consumerKeyState  = valid
      this.model.consumerSecretState  = valid
      this.model.typeState  = valid
      this.model.srcAccountState  = valid
      this.model.productsState  = valid
      this.model.isactiveState  = valid
      return valid
    },
    resetModal() {
      // this.model.userId = ''
      this.model.name = ''
      this.model.consumerKey = ''
      this.model.consumerSecret = ''
      this.model.srcAccount = ''
      this.model.products = []
      this.model.isactive = true,
      this.model.userIdState = null
      this.model.nameState = null
      this.model.consumerKeyState = null
      this.model.consumerSecretState = null
      this.model.typeState = null
      this.model.srcAccountState = null
      this.model.productsState = null
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
    handleOKnewApps(bvModalEvt) {
      bvModalEvt.preventDefault()
      this.handleSubmitnewApps()
    },
    handleSubmitnewApps() {
      if (!this.checkFormValidity()) {
        return
      }
      this.$nextTick(() => {
        this.createNewApps()
        this.$bvModal.hide('newApps')
      })
    },
  },
  computed: {
    dataReady() {
      return this.isLoading && this.isLoadingProducts
    }
  },
};
</script>

<style src="./Apps.scss" lang="scss" />
