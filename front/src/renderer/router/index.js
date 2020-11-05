import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const routes = [
  {
    path: '/',
    name: 'start',
    component: () => import('../components/Start')
  },
  {
    path: '/editor',
    name: 'editor',
    component: () => import('../components/Editor')
  },
  {
    path: '/tray',
    name: 'tray',
    component: () => import('../components/Tray')
  }
]

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
