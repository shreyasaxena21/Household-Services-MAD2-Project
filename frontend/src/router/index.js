import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import register from "@/views/RegisterView.vue"
import admindashboard from "@/views/Admindashboard.vue"


const routes = [
  {
    path: '/',
    name: 'home',
    component : import('@/views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "about" */ '../views/LoginView.vue')
  },
  {
    path: '/Register',
    name: 'register',
    component: register
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path : '/addService',
    name : 'addService',
    component : () => import('@/views/AddService.vue')
  },
  {
    name: 'updateService',
    path: '/updateService/:id',
    component: () => import('@/views/UpdateService.vue')
  },
  {
    name: 'admindashboard',
    path: '/admindashboard',
    component: () => import('@/views/Admindashboard.vue')
  },
  {
    name: 'professionaldashboard',
    path: '/professionaldashboard',
    component: () => import('@/views/ProfessionalDashboard.vue')
  },
  {
    name: 'customerdashboard',
    path: '/customerdashboard',
    component: () => import('@/views/CustomerDashboard.vue')
  },
  {
    name : 'service',
    path: '/service',
    component : () => import('@/views/Service.vue')
  },
  {
    name : 'updateservicerequest',
    path: '/updateservicerequest/:id',
    component : () => import('@/views/UpdateServiceRequest.vue')
  },
  {
    name : 'closeservicerequest',
    path: '/closeservicerequest/:id',
    component : () => import('@/views/CloseServiceRequest.vue')
  },
  {
    name : 'adminsearch',
    path: '/adminsearch',
    component : () => import('@/views/AdminSearch.vue')
  },
  {
    name: "adminstats",
    path: "/showadminsstats",
    component: () => import("@/views/showadminsstats.vue"),
  },
  {
    name : 'editcustomerprofile',
    path: '/editcustomerprofile',
    component : () => import('@/views/EditCustomerProfile.vue')
  },
  {
    name : 'editprofessionalprofile',
    path: '/editprofessionalprofile',
    component : () => import('@/views/EditProfessionallProfile.vue')
  },

  {
    name : 'customersearch',
    path: '/customersearch',
    component : () => import('@/views/customersearch.vue')
  },

  {
    name : 'profstats',
    path: '/profstats',
    component : () => import('@/views/showprofessionalstats.vue')
  },

  


  
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
