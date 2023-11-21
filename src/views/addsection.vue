<template>
  <div class="container">
    <div class="jumbotron text-center">
      <!-- <img src="/static/pic3.png"> -->
      <h1>Add a Category</h1>

      <br />
      <form @submit.prevent="add">
        <div class="form-group">
          <input
            type="text"
            class="form-control"
            id="name"
            placeholder="Enter Category Name"
            v-model="section.name"
            required
          />
        </div>

        <div class="form-group">
          <button type="submit" class="btn btn-primary">ADD</button>
        </div>
      </form>
    </div>
  </div>
</template>
<script setup>
import { ref, reactive, onBeforeMount } from 'vue'
import ProductField from '@/components/ProductField.vue'
import customfetch from '../modules/customfetch'
import router from '../router'
const loggedin = localStorage.getItem('loggedin')
const role = localStorage.getItem('user')
onBeforeMount(() => {
  if (loggedin != 'true') {
    alert('Unauthorized access\nRedirecting to Home Page')
  } else if (loggedin == 'true' && role != 'admin') {
    router.push('/')
  }
})

const section = reactive({
  name: ''
})
function add() {
  customfetch('http://127.0.0.1:5000/addsection', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-access-token': localStorage.getItem('token')
    },

    body: JSON.stringify({ name: section.name })
  })
    .then((data) => {
      if (data) {
        alert('Section added successfully')
        router.push('/adminpanel')
      } else {
        alert('Section already exists')
      }
    })
    .catch((err) => {
      console.log(err)
      alert(err.message)
    })
}
</script>
<style></style>
