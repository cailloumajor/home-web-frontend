import Vue from 'vue'
import Router from 'vue-router'

const Heating = resolve => require(['../pages/Heating'], resolve)

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/heating',
      component: Heating,
      meta: {
        title: 'Chauffage'
      }
    }
  ]
})

router.afterEach(route => {
  document.title = route.meta.title + ' - Home Web'
})

export default router
