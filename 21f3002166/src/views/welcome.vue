<template>
  <div class="container">
    <div class="jumbotron text-center">
      <h1><b>Welcome to EMarket</b></h1>

      <h4>Your favorite Grocery Store</h4>
      <br />
      <h4>Already a user?</h4>

      <router-link class="btn btn-primary btn-lg" to="/clogin">Log In</router-link>
      <br />
      <br />

      <h4>Don't have an account?</h4>

      <router-link class="btn btn-primary btn-lg" to="/signup">Sign Up</router-link>
    </div>
  </div>
</template>
<script setup>
import { onBeforeMount } from 'vue'
import router from '../router/index'
const loggedin = localStorage.getItem('loggedin')

onBeforeMount(() => {
  if (loggedin == 'true') {
    const u = localStorage.getItem('user')
    switch (u) {
      case 'customer':
        router.push('/market')
        break
      case 'storem':
        router.push('/storempanel')
        break
      case 'admin':
        router.push('/adminpanel')
        break
      default:
        router.push('/')
    }
  }
})
</script>
<style>
.jumbotron {
  font-family: cursive;

  background-image: url('@/assets/BGimg3.jpg');
  background-size: 100% 100%;
  background-attachment: fixed;
  background-repeat: no-repeat;
}
.container {
  display: flex;
  justify-content: center;
  padding-top: 100px;
}
</style>
