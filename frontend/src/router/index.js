import { createRouter, createWebHashHistory } from 'vue-router'
// import Home from '../views/Home.vue'
import About from '../views/About.vue'
import TestBoard from '../views/TestBoard.vue'
// import MainContent from '../views/MainContent.vue'

const routes = [
  {
    path: '/',
    name: 'TestBoard',
    component: TestBoard
  },
  {
    path: '/About',
    name: 'About',
    component: About
  }
]

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes
})

export default router
