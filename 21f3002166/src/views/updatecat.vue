<template>
  <div>
    <h2>Update Category</h2>
    <div class="container">
      <div class="jumbotron text-center">
        <form @submit.prevent="updatecategory">
          <div class="form-group">
            <label for="name">Name:</label>
            <input v-model="name" type="text" class="form-control" id="name" required />
          </div>

          <button type="submit" class="btn btn-primary">Update Category</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeMount } from 'vue'
import customfetch from '../modules/customfetch'
import router from '../router/index'
import { useRoute } from 'vue-router'
const route = useRoute()
const name = ref('')
const loggedin = localStorage.getItem('loggedin')
const user = localStorage.getItem('user')

onBeforeMount(() => {
  if (loggedin != 'true') {
    alert('Login to continue')
    router.push('/alogin')
  } else if (loggedin == 'true' && user != 'admin') {
    router.push('/')
  }
})

onMounted(async () => {
  try {
    const catid = route.params.id
    const catresponse = await customfetch(`http://127.0.0.1:5000/getcategory/${catid}`, {
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      }
    })

    name.value = catresponse.name
  } catch (error) {
    console.error('An error occurred:', error)
    alert(error.message)
  }
})

const updatecategory = async () => {
  try {
    const catid = route.params.id
    const response = await customfetch(`http://127.0.0.1:5000/updatecat/${catid}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      },
      body: JSON.stringify({
        name: name.value
      })
    })
      .then((data) => {
        if (data) {
          alert('Category updated successfully')
          router.push('/categories')
        }
      })
      .catch((err) => {
        console.log(err)
        alert(err.message)
      })
  } catch (error) {
    console.error('An error occurred:', error)
    alert(error.message)
  }
}
</script>
<style>
.jumbotron {
  /* background-image: url("@/assets/BGimg3.jpg"); */
  font-family: cursive;
}
.container {
  display: flex;
  justify-content: center;
  padding-top: 100px;
}
</style>
