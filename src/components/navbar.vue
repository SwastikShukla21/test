<template>
  <nav class="navbar navbar-expand-md">
    <router-link class="navbar-brand" to="/"
      ><img src="../assets/pic.png" style="width: 50px"
    /></router-link>
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarNav"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav mr-auto"></ul>
      <ul class="navbar-nav">
        <li v-for="link in links" :key="link.to" class="nav-item">
          <router-link class="nav-link" :to="link.path">{{ link.name }} </router-link>
        </li>
      </ul>
      <ul class="navbar-nav">
        <li v-if="checklogin()" class="nav-item">
          <div class="nav-link" @click="logout">LOG OUT</div>
        </li>
      </ul>
    </div>
  </nav>
</template>
<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import router from '../router/index'

const route = useRoute()
function checklogin() {
  return localStorage.getItem('loggedin') === 'true'
}

const logout = () => {
  confirm('Are you sure you want to logout?')
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  localStorage.removeItem('loggedin')
  localStorage.removeItem('username')
  router.push('/')
}
const links = computed(() => {
  switch (route.name) {
    case 'welcome':
      return [
        { name: 'Home', path: '/' },
        { name: 'Admin Log In', path: '/alogin' },
        { name: 'Store Manager Log In', path: '/slogin' }
      ]
    case 'market':
      return [{ name: 'Orders', path: '/orders' }]
    case 'Login':
      return [
        { name: 'Home', path: '/' },
        { name: 'Signup', path: '/signup' }
      ]
    case 'Signup':
      return [
        { name: 'Home', path: '/' },
        { name: 'Login', path: '/clogin' }
      ]
    case 'storempanel':
      return [
        { name: 'Home', path: '/' },
        { name: 'All Orders', path: '/orders' }
      ]
    case 'addmanager':
      return [
        { name: 'Home', path: '/' },
        { name: 'Admin Panel', path: '/adminpanel' }
      ]
    case 'adminlogin':
      return [
        { name: 'Home', path: '/' },
        { name: 'Store Manager Log In', path: '/slogin' }
      ]
    case 'storem':
      return [
        { name: 'Home', path: '/' },

        { name: 'Admin Login', path: '/alogin' }
      ]
    case 'updatecat':
      return [
        { name: 'Admin Panel', path: '/adminpanel' },
        { name: 'Categories', path: '/categories' },
        { name: 'Add Category', path: '/addsection' }
      ]
    case 'categories':
      return [
        { name: 'Admin Panel', path: '/adminpanel' },
        { name: 'Add Category', path: '/addsection' }
      ]
    case 'addsection':
      return [
        { name: 'Admin Panel', path: '/adminpanel' },
        { name: 'Show Categories', path: '/categories' }
      ]
    case 'addproduct':
      return [
        { name: 'Manager Panel', path: '/storempanel' },
        { name: 'Show Products', path: '/products' }
      ]
    case 'adminrequests':
      return [{ name: 'Admin Panel', path: '/adminpanel' }]
    case 'products':
      return [
        { name: 'Manager Panel', path: '/storempanel' },
        { name: 'Add Product', path: '/addproduct' }
      ]
    case 'Storemrequest':
      return [{ name: 'Manager Panel', path: '/storempanel' }]
    case 'orders':
      return [{ name: 'Home', path: '/' }]
    case 'adminpanel':
      return [{ name: 'Add Store Manager', path: '/addmanager' }]
    case 'summary':
      return [{ name: 'Manager Panel', path: '/storempanel' }]

    default:
      return []
  }
})
</script>
<style scoped>
.navbar {
  background-color: yellow;
  font-family: Georgia, 'Times New Roman', Times, serif;
}
.navbar a {
  color: green;
}
</style>
