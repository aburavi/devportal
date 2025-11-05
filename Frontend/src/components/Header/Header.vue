<template>
  <b-navbar class="header d-print-none app-header">
    <b-nav>
      <b-nav-item>
        <a class="d-md-down-none px-2" href="#" @click="toggleSidebarMethod" id="barsTooltip">
          <i class='fi flaticon-menu' />
        </a>
        <a class="fs-lg d-lg-none" href="#" @click="switchSidebarMethod">
          <i class='fi flaticon-menu' />
        </a>
      </b-nav-item>
      <b-nav-item class="d-md-down-none">
        <a href="#" class="px-2">
          <i class='fi flaticon-flip' />
        </a>
      </b-nav-item>
      <b-nav-item class="d-md-down-none">
        <a href="#" class="px-2">
          <i class='fi flaticon-close' />
        </a>
      </b-nav-item>
    </b-nav>
    <b-nav>
      <b-form class="d-sm-down-none ml-5" inline>
        <b-form-group>
          <b-input-group class="input-group-no-border">
            <template v-slot:prepend>
              <b-input-group-text><i class='fi flaticon-search-2'/></b-input-group-text>
            </template>
            <b-form-input id="search-input" placeholder="Search" />
          </b-input-group>
        </b-form-group>
      </b-form>
    </b-nav>
    <a class="navbarBrand d-md-none">
      <i class="fa fa-circle text-danger" />
      &nbsp;
      POS
      &nbsp;
      <i class="fa fa-circle text-primary" />
    </a>
    <b-nav class="ml-auto">
      <b-nav-item-dropdown
        class="notificationsMenu d-sm-down-none mr-2"
        menu-class="notificationsWrapper py-0 animate__animated animate__animated-fast animate__fadeIn"
        right>
        <template slot="button-content">
          <span class="avatar rounded-circle thumb-sm float-left mr-2">
            <img class="rounded-circle" :src="model.avatar" alt="..." />
          </span>
          <span class="px-2">{{ model.firstname }}  {{ model.lastname }}</span>
        </template>
      </b-nav-item-dropdown>
      <b-nav-item-dropdown id="v-step-2" class="settingsDropdown d-sm-down-none" no-caret right>
        <template slot="button-content">
          <i class='fi flaticon-settings-10 px-2' />
        </template>
        <b-dropdown-item><i class='fi flaticon-person px-3 mr-3' /> My Account</b-dropdown-item>
        <b-dropdown-divider />
        <b-dropdown-item-button @click="logout">
          <i class="fi flaticon-power-1 px-3 mr-3" /> Log Out
        </b-dropdown-item-button>
      </b-nav-item-dropdown>
    </b-nav>
  </b-navbar>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import Notifications from '@/components/Notifications/Notifications';
import jwt_decode from 'jwt-decode'

export default {
  name: 'Header',
  components: { Notifications },
  data() {
    return {
      model: {
        avatar: '',
        firstname: '',
        lastname: '',
      }
    }
  },
  created() {
    let token = window.localStorage.getItem('openapi-token')
    let decoded_token = jwt_decode(token);
    this.model.firstname = decoded_token.given_name
    this.model.lastname = decoded_token.family_name
    this.model.avatar = decoded_token.avatar
  },
  computed: {
    ...mapState('layout', ['sidebarClose', 'sidebarStatic']),
  },
  methods: {
    ...mapActions('layout', ['toggleSidebar', 'switchSidebar', 'changeSidebarActive']),
    switchSidebarMethod() {
      if (!this.sidebarClose) {
        this.switchSidebar(true);
        this.changeSidebarActive(null);
      } else {
        this.switchSidebar(false);
        const paths = this.$route.fullPath.split('/');
        paths.pop();
        this.changeSidebarActive(paths.join('/'));
      }
    },
    toggleSidebarMethod() {
      if (this.sidebarStatic) {
        this.toggleSidebar();
        this.changeSidebarActive(null);
      } else {
        this.toggleSidebar();
        const paths = this.$route.fullPath.split('/');
        paths.pop();
        this.changeSidebarActive(paths.join('/'));
      }
    },
    logout() {
      window.localStorage.setItem('openapi-authenticated', false);
      window.localStorage.removeItem('openapi-roles');
      window.localStorage.removeItem('openapi-token');
      window.localStorage.removeItem('openapi-username');
      window.localStorage.removeItem('openapi-exp');
      this.$router.replace('/login');
    },
  }
};
</script>

<style src="./Header.scss" lang="scss"></style>
