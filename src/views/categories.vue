<template>
  <div>
    <div class="container">
      <div class="jumbotron text-center">
        <h2>Categories</h2>
        <div>
          <table>
            <thead>
              <tr id="top">
                <th>Category Name</th>

                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="category in categories" :key="category.id">
                <td>{{ category.name }}</td>

                <td>
                  <button @click="editcategory(category.id)" class="btn btn-primary">Edit</button>
                  <button @click="deletecategory(category.id)" class="btn btn-danger">
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, onBeforeMount } from 'vue'
import router from '../router/index'
import customfetch from '../modules/customfetch'
const role= localStorage.getItem('user')
const categories = ref([])

const loggedin = localStorage.getItem('loggedin')
onBeforeMount(() => {
  if (loggedin != 'true') {
    alert('Unauthorized access\nRedirecting to Home Page')
    router.push('/')
  } else if (loggedin == 'true' && role=='customer') {
    router.push('/')
  }
})

onMounted(async () => {
  try {
    const response = await customfetch('http://127.0.0.1:5000/categories', {
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      }
    })
    categories.value = response
  } catch (error) {
    console.log(error.message)
    alert(error.message)
  }
})

const editcategory = (catid) => {
  router.push(`/updatecat/${catid}`)
}

async function deletecategory(catid) {
  if (confirm('Are you sure you want to delete this Category?')) {
    try {
      const response = await customfetch(`http://127.0.0.1:5000/deletecat/${catid}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'x-access-token': localStorage.getItem('token')
        }
      })
        .then((data) => {
          if (data) {
            alert('Category deleted successfully')
            router.push('/adminpanel')
          }
        })
        .catch((err) => {
          console.log(err)
          alert(err.message)
        })
    } catch (error) {
      console.error('An error occurred:', error)
    }
  }
}
</script>
<style>
.jumbotron {
  font-family: cursive;
}
.container {
  display: flex;
  justify-content: center;
  padding-top: 100px;
}
.p a {
  color: green;
}
tr {
  border-bottom: 1px solid black;
}
th {
  text-align: center;
  padding: 10px;
}
td {
  padding: 10px;
}
table {
  display: block;
  border-spacing: 10px;
  border: 2px solid black;
  background-color: rgb(255, 255, 100);
}
#top {
  border-top: 1px solid black;
  font-weight: bold;
  background-color: greenyellow;
}
#top th {
  border-top: 1px solid black;
  font-weight: bold;
  background-color: greenyellow;
}
</style>
