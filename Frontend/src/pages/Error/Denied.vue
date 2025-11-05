<template>
  <div class="denied-page">
    <b-container>
      <div class="errorContainer mx-auto">
        <h1 class="errorCode">403</h1>
        <p class="errorInfo">
            Opps, it seems that you Permissions Denied.
        </p>
        <p class="errorHelp mb-3">
            If you are sure it should, chek your permission roles.
        </p>
        <b-form>
          <router-link :to="model.cmd">
            <b-button class="errorBtn" type="submit" variant="success">
                Back to Home <i class="la la-home ml-xs" />
            </b-button>
          </router-link>
        </b-form>
      </div>
      <footer class="pageFooter">
        2022 &copy; OpenApi App Vue Admin OpenAPI.
      </footer>
    </b-container>
  </div>
</template>

<script>
export default {
  name: 'DeniedPage',
  data() {
    return {
      model: {
        cmd: '',
      }
    }
  },
  created() {
    let roles = window.localStorage.getItem('openapi-roles');
    if (roles) {
      if (roles.indexOf('admin') != -1) {
        this.model.cmd = '/app/home';
      } else if (roles.indexOf('tenant') != -1) {
        this.model.cmd = '/tenant/home';
      } else {
        this.model.cmd = '/login';
      }
    }
  },
};
</script>

<style src="./Error.scss" lang="scss" scoped />
