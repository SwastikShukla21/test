// StoreManager.vue
<template>
  <div class="container">
    <div class="jumbotron text-center">
      <h2>Categories</h2>
      <br />
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
              <button @click="editcategory(category)" class="btn btn-primary">Edit</button>
              <button @click="deletecategory(category)" class="btn btn-danger">Delete</button>
            </td>
          </tr>
          <button class="btn btn-primary" @click="addCategory">Add Category</button>
        </tbody>
      </table>
    </div>
  </div>

  <div class="container">
    <div class="jumbotron text-center">
      <h2>Previous Requests</h2>
      <div v-if="requests.length === 0">
        <h4>No previous requests to show</h4>
      </div>

      <div v-else>
        <br />
        <table>
          <thead>
            <tr id="top">
              <th>Type</th>
              <th>Subtype</th>
              <th>Category</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in requests" :key="request.id">
              <td>{{ request.type }}</td>
              <td>{{ request.subtype }}</td>
              <td>{{ request.sectionname }}</td>
              <td>{{ request.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeMount } from 'vue'
import customfetch from '../modules/customfetch'
import router from '../router'

const categories = ref([])
const requests = ref([])

const categoriesCount = computed(() => categories.value.length)
const requestsCount = computed(() => requests.value.length)

const loggedin = localStorage.getItem('loggedin')
const user = localStorage.getItem('user')
onBeforeMount(() => {
  if (loggedin != 'true') {
    alert('Login to continue,')
    router.push('/slogin')
  } else if (loggedin == 'true' && user != 'storem') {
    alert('Unauthorized access!!!\nNot a store Manger Redirecting to Home page')
    router.push('/')
  }
})
onMounted(async () => {
  try {
    customfetch('http://127.0.0.1:5000/categories', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then((response) => {
        categories.value = response
      })
      .catch((error) => {
        console.log(error.message)
        alert(error.message)
      })
    customfetch('http://127.0.0.1:5000/requests', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      }
    })
      .then((response) => {
        requests.value = response
      })
      .catch((error) => {
        console.log(error.message)
        alert(error.message)
      })
  } catch (error) {
    console.log(error)
    alert(error)
  }
})

async function addCategory() {
  try {
    const name = prompt('Enter the category name')
    if (!name) return

    const category = { name }

    const newname = name

    const request = {
      type: 'Category Management',
      subtype: 'add',
      status: 'pending',
      newname: newname
    }
    //
    requests.value.push(request)
    customfetch('http://127.0.0.1:5000/requests', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      },
      body: JSON.stringify(request)
    })
      .then((response) => {
        console.log(response)
        alert(response.message)
        router.push('/storemrequest')
      })
      .catch((error) => {
        console.log(error.message)
        alert(error.message)
      })
  } catch (error) {
    console.error(error)
  }
}

function editcategory(category) {
  try {
    const name = prompt('Enter the new category name', category.name)
    if (!name) return

    const newname = name

    const request = {
      id: category.id,
      type: 'Category Management',
      subtype: 'update',
      status: 'pending',
      newname: newname
    }

    requests.value.push(request)
    customfetch('http://127.0.0.1:5000/requests', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      },
      body: JSON.stringify(request)
    })
      .then((response) => {
        console.log(response)
        alert(response.message)
        router.push('/storemrequest')
      })
      .catch((error) => {
        console.log(error.message)
        alert(error.message)
      })
  } catch (error) {
    console.error(error)
  }
}

async function deletecategory(category) {
  try {
    // confirm with the user before deleting
    const confirmed = confirm(`Are you sure you want to delete ${category.name}?`)
    if (!confirmed) return
    else {
      customfetch(`http://127.0.0.1:5000/requests`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-access-token': localStorage.getItem('token')
        },
        body: JSON.stringify({
          id: category.id,
          type: 'Category Management',
          subtype: 'delete',
          status: 'pending',
          newname: category.name
        })
      })
        .then((response) => {
          console.log(response)
          alert(response.message)
          router.push('/storemrequest')
        })
        .catch((error) => {
          console.log(error.message)
          alert(error.message)
        })
    }
  } catch (error) {
    console.error('An error occurred:', error)
  }
}
</script>
<style>
tr {
  border-bottom: 1px solid black;
}
th {
  text-align: center;
  font-weight: bold;
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
.jumbotron {
  font-family: cursive;
}
.container {
  display: flex;
  justify-content: center;
  padding-top: 100px;
}
#top th {
  border-top: 1px solid black;
  font-weight: bold;
  background-color: greenyellow;
}
</style>
