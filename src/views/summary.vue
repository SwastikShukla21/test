<template>
  <div class="container-lg" id="main">
    <br />
    <h1>Summary</h1>
    <div class="jumbotron text">
      <!-- <img src="/static/pic3.png"> -->
      <div class="row">
        <div class="col-md-6">
          <div class="container-md" id="child">
            <h3>Category Wise Sales</h3>
            <br />
            <img :src="catwisesales" alt="category" width="640" height="480" />
            <br />
          </div>
        </div>
        <div class="col-md-6">
          <div class="container-md" id="child">
            <h3>Daytime Wise Sales</h3>
            <br />
            <img :src="timeorder" alt="timeser" width="640" height="480" />

            <br />
          </div>
        </div>
      </div>

      <br />

      <br />
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref, onBeforeMount } from 'vue'
import router from '../router/index'
import customfetch from '../modules/customfetch'
let timeorder = 'backend/static/order_timeseries.jpg'
let catwisesales = 'backend/static/catwisesales.jpg'
const loggedin = localStorage.getItem('loggedin')
const user = localStorage.getItem('user')
onBeforeMount(() => {
  if (loggedin != 'true') {
    alert('Login to continue,')
    router.push('/')
  } else if (loggedin == 'true' && user != 'storem') {
    router.push('/')
  }
})
onMounted(() => {
  const response = customfetch('http://127.0.0.1:5000/summary', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'x-access-token': localStorage.getItem('token')
    }
  }).then((response) => console.log(response))
  timeorder = 'backend/static/order_timeseries.jpg'
  catwisesales = 'backend/static/catwisesales.jpg'
})
</script>
