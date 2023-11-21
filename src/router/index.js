import { createRouter, createWebHistory } from 'vue-router'
import updateproduct from '../views/updateproduct.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'welcome',
      component: () => import('../views/welcome.vue')
    },
    {
      path: '/clogin',
      name: 'Login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/signup',
      name: 'Signup',
      component: () => import('../views/SignUp.vue')
    },
    {
      path: '/market',
      name: 'market',
      component: () => import('../views/market.vue')
    },
    {
      path: '/alogin',
      name: 'adminlogin',
      component: () => import('../views/adminlogin.vue')
    },
    {
      path: '/slogin',
      name: 'storem',
      component: () => import('../views/storemlogin.vue')
    },
    {
      path: '/adminpanel',
      name: 'adminpanel',
      component: () => import('../views/adminpanel.vue')
    },
    {
      path: '/storempanel',
      name: 'storempanel',
      component: () => import('../views/storempanel.vue')
    },
    {
      path: '/addsection',
      name: 'addsection',
      component: () => import('../views/addsection.vue')
    },
    {
      path: '/addproduct',
      name: 'addproduct',
      component: () => import('../views/addproduct.vue')
    },
    {
      path: '/products',
      name: 'products',
      component: () => import('../views/products.vue')
    },
    {
      path: '/updateproduct/:id',
      name: 'updateproduct',
      component: updateproduct
    },
    {
      path: '/getproduct/:id',
      name: 'getproduct'
    },
    {
      path: '/categories',
      name: 'categories',
      component: () => import('../views/categories.vue')
    },
    {
      path: '/updatecat/:id',
      name: 'updatecat',
      component: () => import('../views/updatecat.vue')
    },
    {
      path: '/storemrequest',
      name: 'Storemrequest',
      component: () => import('../views/storemrequest.vue')
    },
    {
      path: '/adminrequests',
      name: 'adminrequests',
      component: () => import('../views/adminrequests.vue')
    },
    {
      path: '/addmanager',
      name: 'addmanager',
      component: () => import('../views/addmanager.vue')
    },
    {
      path: '/orders',
      name: 'orders',
      component: () => import('../views/orders.vue')
    },
    { path: '/summary', name: 'summary', component: () => import('../views/summary.vue') }
  ]
})

export default router
