<template>
  <div class="sidebar-wrapper" v-if="model.roles === 'admin'">
    <nav
        :class="{sidebar: true, sidebarStatic, sidebarOpened}"
        @mouseenter="sidebarMouseEnter"
        @mouseleave="sidebarMouseLeave"
    >
      <header class="logo">
        <router-link to="/app/home"><span class="primary-word">POS</span> <span class="secondary-word"> OpenAPI</span></router-link>
      </header>

      <h5 class="navTitle first">
        Admin Menu
      </h5>
      <ul class="nav">
        <NavLink
            :activeItem="activeItem"
            header="Home"
            link="/app/home"
            iconName="flaticon-home"
            index="home"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="Profile"
            link="/app/profile"
            iconName="flaticon-user"
            index="profile"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="Tenants"
            link="/app/tenants"
            iconName="flaticon-menu"
            index="tenants"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="Apps"
            link="/app/apps"
            iconName="flaticon-app"
            index="apps"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="Approved"
            link="/app/approved"
            iconName="flaticon-checked"
            index="approved"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="SIT-Request"
            link="/app/productions"
            iconName="flaticon-layers"
            index="sit-request"
            isHeader
        />    
        <NavLink
            :activeItem="activeItem"
            header="SignatureGen"
            link="/app/siggen"
            iconName="flaticon-calculator"
            index="signaturegen"
            isHeader
        />          
        <NavLink
            :activeItem="activeItem"
            header="Documentations"
            link="/app/documentations"
            iconName="flaticon-document"
            index="documentations"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="FAQs"
            link="/app/faqs"
            iconName="flaticon-list"
            index="faqs"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="Log Status"
            link="/app/logs"
            iconName="flaticon-flip"
            index="logs"
            isHeader
        />
      </ul>
    </nav>
  </div>
  <div class="sidebar-wrapper" v-else>
    <nav
        :class="{sidebar: true, sidebarStatic, sidebarOpened}"
        @mouseenter="sidebarMouseEnter"
        @mouseleave="sidebarMouseLeave"
    >
      <header class="logo">
        <router-link to="/app/home"><span class="primary-word">POS</span> <span class="secondary-word"> OpenAPI</span></router-link>
      </header>

      <h5 class="navTitle first">
        Tenant Menu
      </h5>
      <ul class="nav">
        <NavLink
            :activeItem="activeItem"
            header="Home"
            link="/tenant/home"
            iconName="flaticon-home"
            index="home"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="Profile"
            link="/tenant/profile"
            iconName="flaticon-user"
            index="profile"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="Apps"
            link="/tenant/apps"
            iconName="flaticon-app"
            index="apps"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="SIT-Request"
            link="/tenant/productions"
            iconName="flaticon-layers"
            index="sit-request"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="SignatureGen"
            link="/tenant/siggen"
            iconName="flaticon-calculator"
            index="signaturegen"
            isHeader
        />      
        <NavLink
            :activeItem="activeItem"
            header="Documentations"
            link="/tenant/documentations"
            iconName="flaticon-document"
            index="documentations"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="FAQs"
            link="/tenant/faqs"
            iconName="flaticon-list"
            index="faqs"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="Log Status"
            link="/tenant/logs"
            iconName="flaticon-flip"
            index="logs"
            isHeader
        />
      </ul>
    </nav>
  </div>
</template>

<script>
import Widget from '@/components/Widget/Widget';
import { mapState, mapActions } from 'vuex';
import isScreen from '@/core/screenHelper';
import NavLink from './NavLink/NavLink';

export default {
  name: 'Sidebar',
  components: { NavLink, Widget },
  data() {
    return {
      model: {
        roles : '',
      }
    };
  },
  methods: {
    load(){
      this.model.roles = window.localStorage.getItem("openapi-roles");
    },
    ...mapActions('layout', ['changeSidebarActive', 'switchSidebar']),
    setActiveByRoute() {
      const paths = this.$route.fullPath.split('/');
      paths.pop();
      this.changeSidebarActive(paths.join('/'));
    },
    sidebarMouseEnter() {
      if (!this.sidebarStatic && (isScreen('lg') || isScreen('xl'))) {
        this.switchSidebar(false);
        this.setActiveByRoute();
      }
    },
    sidebarMouseLeave() {
      if (!this.sidebarStatic && (isScreen('lg') || isScreen('xl'))) {
        this.switchSidebar(true);
        this.changeSidebarActive(null);
      }
    },
  },
  created() {
    this.load();
    this.setActiveByRoute();
  },
  computed: {
    ...mapState('layout', {
      sidebarStatic: state => state.sidebarStatic,
      sidebarOpened: state => !state.sidebarClose,
      activeItem: state => state.sidebarActiveElement,
    }),
  },
};
</script>

<!-- Sidebar styles should be scoped -->
<style src="./Sidebar.scss" lang="scss" scoped/>
