import Vue from 'vue'
import Router from 'vue-router'
import routes from './routes'

Vue.use(Router)
let uroles = []

// Routing logic
var router = new Router({
  routes: routes,
  mode: "abstract",
})

// Some middleware to help us ensure the user is authenticated.
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (window.localStorage.getItem("openapi-token") == null) {
      // this route requires auth, check if logged in
      // if not, redirect to login page.
      next('/login')
      // window.console.log('not Authenticated')
    } else {
      let roles = window.localStorage.getItem("openapi-roles");
      if (roles) {
        uroles = roles.split(',')
      }
      if (to.meta.permissions && to.meta.permissions.length > 0) {
        let isAllowed = uroles.some(p => to.meta.permissions.includes(p))        
        if (! isAllowed) return next('/denied')
        else return next()
      }
    }
  } else {
    next()
  }
})

export default router
