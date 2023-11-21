<template>
  <h1 style="text-align: center">Admin Panel</h1>
  <div class="container">
    <div class="jumbotron text-center">
      <div v-if="requests.length === 0">
        <h6>No Requests to show</h6>
      </div>
      <div v-else>
        <br />
        <h2>Pending Requests</h2>
        <div v-if="pendingRequests().length === 0">
          <h6>No Pending Requests</h6>
        </div>
        <div v-else>
          <table>
            <thead>
              <tr id="top">
                <th>Request Type</th>
                <th>Request Subtype</th>
                <th>Category Name</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in pendingRequests()" :key="request.id">
                <td>{{ request.type }}</td>
                <td>{{ request.subtype }}</td>
                <td>{{ request.sectionname }}</td>
                <td>{{ request.status }}</td>
                <td>
                  <button class="btn btn-primary" @click="acceptRequest(request)">Accept</button>
                  <button class="btn btn-danger" @click="rejectRequest(request)">Reject</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <br />
        <br />
        <h2>Previous Requests</h2>
        <table>
          <thead>
            <tr id="top">
              <th>Request Type</th>
              <th>Request Subtype</th>
              <th>Category Name</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in previousRequests()" :key="request.id">
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
import { ref, onMounted,onBeforeMount } from 'vue'
import customfetch from '@/modules/customfetch'
import router from '@/router/index'
const loggedin = localStorage.getItem('loggedin')
const role=localStorage.getItem('user')
const requests = ref([])
onBeforeMount(()=>{
  if(loggedin!='true')
  {
    alert('Unauthorized access\nRedirecting to Home Page')

  }
  else if(loggedin=='true' && role!='admin')
    { 
      router.push('/')
    }
})
onMounted(async () => {
  try {
    const response = await customfetch('http://127.0.0.1:5000/requests', {
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      }
    })
    requests.value = response
  } catch (error) {
    console.error(error)
    alert(error.message)
  }
})

async function acceptRequest(request) {
  try {
    if (request.type == 'Category Management') {
      switch (request.subtype) {
        case 'add':
          customfetch('http://127.0.0.1:5000/addsection', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'x-access-token': localStorage.getItem('token')
            },

            body: JSON.stringify({ name: request.sectionname })
          })
            .then((data) => {
              if (data) {
                alert('Section added successfully')
                request.status = 'Accepted'
                customfetch('http://127.0.0.1:5000/requests', {
                  method: 'PUT',
                  headers: {
                    'Content-Type': 'application/json',
                    'x-access-token': localStorage.getItem('token')
                  },
                  body: JSON.stringify({
                    id: request.id,
                    status: request.status
                  })
                })

                router.push('/adminpanel')
              } else {
                alert('Section already exists')
              }
            })
            .catch((err) => {
              console.log(err)
              alert(err.message)
            })
          break
        case 'update':
          customfetch(`http://127.0.0.1:5000/updatecat/${request.cat_id}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'x-access-token': localStorage.getItem('token')
            },
            body: JSON.stringify({
              name: request.sectionname
            })
          })
            .then((data) => {
              if (data) {
                alert('Category updated successfully')
                request.status = 'Accepted'
                customfetch('http://127.0.0.1:5000/requests', {
                  method: 'PUT',
                  headers: {
                    'Content-Type': 'application/json',
                    'x-access-token': localStorage.getItem('token')
                  },
                  body: JSON.stringify({
                    id: request.id,
                    status: request.status
                  })
                })

                router.push('/adminpanel')
              }
            })
            .catch((err) => {
              console.log(err)
              alert(err.message)
            })

          break
        case 'delete':
          if (confirm('Are you sure you want to delete this Category?'))
            await customfetch(`http://127.0.0.1:5000/deletecat/${request.cat_id}`, {
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
          break
        default:
          break
      }
    }
  } catch (error) {
    console.error(error)
  }
}
function pendingRequests() {
  return requests.value.filter((request) => request.status === 'pending')
}
function previousRequests() {
  return requests.value.filter((request) => request.status !== 'pending')
}
async function rejectRequest(request) {
  try {
    request.status = 'Rejected'
    customfetch('http://127.0.0.1:5000/requests', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      },
      body: JSON.stringify({
        status: request.status,
        id: request.id
      })
    }).then((data) => {
      if (data) {
        alert('Request Rejected')
        router.push('/adminpanel')
      }
    })
  } catch (error) {
    console.error(error)
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
