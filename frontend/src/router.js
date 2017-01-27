import Vue from 'vue'
import VueRouter from 'vue-router'

const Heating = resolve => require(['./pages/Heating'], resolve)

Vue.use(VueRouter)

const routes = [
  {
    path: '/heating',
    component: Heating,
    meta: {
      title: 'Chauffage'
    }
  }
]

const router = new VueRouter({
  routes
})

router.afterEach(route => {
  document.title = route.meta.title + ' - Home Web'
})

export default router
