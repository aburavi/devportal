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
                    <th>Owner</th>
                    <th>Apps Name</th>
                    <th>Consumer_key</th>
                    <th>Consumer_secret</th>
                    <th class="hidden-sm-down">AccountNo</th>
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
                      <b-badge variant="info"><small>{{row.type}}</small></b-badge>
                    </td>
                    <td class="text-semi-muted">
                       {{row.consumer_key}}
                    </td>
                    <td class="text-semi-muted">
                      {{row.consumer_secret}}
                    </td>
                    <td class="text-semi-muted">
                      {{row.src_accounts[0]}}
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
            id="newApps"
            ref="modal"
            title="Create New Apps"
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKnewApps"
          >
            <form ref="form" @submit.stop.prevent="handleSubmitnewApps">
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
                label="Type"
                label-for="type-input"
                invalid-feedback="Type is required"
                :state="model.typeState"
                >
                <b-form-select
                  id="type-input"
                  v-model="model.type"
                  :state="model.typeState"
                  :options="typeOptions"
                ></b-form-select>
              </b-form-group>
              <b-form-group
                label="Version"
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
                label="Products"
                label-for="products-input"
                invalid-feedback="Products is required"
                :state="model.productsState"
                >
                <b-form-checkbox-group
                  id="products-input"
                  v-model="model.products"
                  :state="model.productsState"
                  :options="model.selectedProducts"
                ></b-form-checkbox-group>
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
        max: '',
        version: '',
        products: [],
        isactive: true,
        userIdState: null,
        nameState: null,
        versionState: null,
        consumerKeyState: null,
        consumerSecretState: null,
        typeState: null,
        srcAccountState: null,
        productsState: null,
        isactiveState: null,
        userOptions: [],
        srcAccountOptions: [],
        maxState: null,
        productsOptions: [],
        selectedProducts: [],
      },
      typeOptions: [
          { value: 'sandbox', text: 'Sandbox' },
      ],
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
      versionOptions: [
          { value: '1.0', text: 'V1.0' },
          { value: '2.0', text: 'V2.0' },
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
      selectedUser: {},
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      this.getUsers();
      this.getApps();
      this.getProducts();
    },
    profileUser(index) {
      this.selectedUser = this.apps_response[index];
    },
    getSelectedProducts() {
      this.model.selectedProducts = []
      for (let i = 0; i < this.model.productsOptions.length; i++) {
          if (this.model.productsOptions[i].version === this.model.version) {
            this.model.selectedProducts.push({ value: this.model.productsOptions[i].value, text: this.model.productsOptions[i].text})
          }
        }
    },
    async getApps() {
      var url = backend.backendURI + '/api/v1/apps/all?order_type=ASC&limit=100&page=1'
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
    async createNewApps() {
      var url = backend.backendURI + '/api/v1/apps'
      var token = window.localStorage.getItem('openapi-token')
      this.model.srcAccountOptions.push(this.model.srcAccount)
      var data = {
        "user_id": this.model.userId,
        "name": this.model.name + '-' + this.model.type,
        "consumer_key": "",
        "consumer_secret": "",
        "type": this.model.type,
        "src_accounts": this.model.srcAccountOptions,
        "max_rate":  this.model.max,
        "products": this.model.products,
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
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
        this.isLoadingApps = true
      } finally {
        this.isLoadingApps = true;
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
            this.model.productsOptions.push({ value: this.products_response.data[i].uripath, text: this.products_response.data[i].name, version: this.products_response.data[i].version})
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
      this.model.userId = ''
      this.model.name = ''
      this.model.consumerKey = ''
      this.model.consumerSecret = ''
      this.model.type = ''
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
    handleOKprofileInfo(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmitprofileInfo();
    },
    handleSubmitprofileInfo() {
      this.$nextTick(() => {
        this.$bvModal.hide('profileInfo');
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
      return this.isLoadingUser && this.isLoading && this.isLoadingProducts
    }
  },
};
</script>

<style src="./Apps.scss" lang="scss" />
