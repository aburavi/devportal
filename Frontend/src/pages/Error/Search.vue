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
          <b-form-group>
            <b-form-input class="input-no-border" type="text" placeholder="Search Pages" />
          </b-form-group>
          <router-link tag="a" to="/app/extra/search">
            <b-button class="errorBtn" type="submit" variant="success">
                Search <i class="la la-search ml-xs" />
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
};
</script>

<style src="./Error.scss" lang="scss" scoped />
