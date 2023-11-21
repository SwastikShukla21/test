<template>
  <div>
    <div class="container">
      <div class="jumbotron text-center">
        <h1 class="display-4">Add Product</h1>
        <p class="lead">Add a new product to your store</p>
        <hr class="my-4" />
        <p>You can add a new product to your store by filling the form below.</p>

        <form @submit.prevent="addProduct">
          <div class="form-group">
            <label for="name">Product Name:</label>
            <input v-model="name" type="text" class="form-control" id="name" required />
          </div>
          <div class="form-group">
            <label for="quantity">Quantity:</label>
            <input
              v-model.number="quantity"
              type="number"
              class="form-control"
              id="quantity"
              min="0"
              required
            />
          </div>
          <div class="form-group">
            <label for="price">Price:</label>
            <input
              v-model.number="price"
              type="number"
              class="form-control"
              id="price"
              min="0"
              required
            />
          </div>
          <div class="form-group" style="text-align: left">
            <label for="category">Category:</label>
            <select v-model="selectedCategory" id="category">
              <option v-for="category in categories" :key="category.id" :value="category.name">
                {{ category.name }}
              </option>
            </select>
          </div>
          <div class="form-group" style="text-align: left">
            <label for="scale">Measuring Scale:</label>
            <select v-model="selectedScale" id="scale">
              <option v-for="scale in scales" :value="scale.name">{{ scale.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="Expiry Date">Expiry Date:</label>
            <input v-model="expirydate" type="date" class="form-control" id="expirydate" required />
          </div>

          <div class="form-group">
            <label for="description">Brief Description:</label>
            <textarea
              v-model="description"
              class="form-control"
              id="description"
              placeholder="Description"
              required
            ></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Add Product</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeMount } from 'vue'
import customfetch from '../modules/customfetch'
import router from '../router'
const name = ref('')
const quantity = ref(0)
const price = ref(0.0)
const selectedCategory = ref(null)
const selectedScale = ref(null)
const categories = ref([])
const scales = ref([])
const description = ref('')
const expirydate = ref('')
const loggedin = localStorage.getItem('loggedin')
const user = localStorage.getItem('user')
onBeforeMount(() => {
  if (!loggedin) {
    alert('Login to continue,')
    router.push('/slogin')
  } else if (loggedin) {
    if (user != 'storem') {
      alert('Unauthorized access!!!\nNot a store Manger Redirecting to Home page')
      router.push('/')
    }
  }
})

function addProduct() {
  customfetch('http://127.0.0.1:5000/addproduct', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-access-token': localStorage.getItem('token')
    },

    body: JSON.stringify({
      name: name.value,
      quantity: quantity.value,
      price: price.value,
      cat: selectedCategory.value,
      ms: selectedScale.value,
      desc: description.value,
      expdate: expirydate.value
    })
  })
    .then((data) => {
      if (data) {
        alert('Product added successfully')
        router.push('/storempanel')
      }
    })
    .catch((err) => {
      console.log(err)
      alert(err.message)
    })
}

onMounted(async () => {
  try {
    const categoriesresp = await customfetch('http://127.0.0.1:5000/categories', {
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      }
    })

    categories.value = categoriesresp

    const scaleresp = await customfetch('http://127.0.0.1:5000/getscale', {
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      }
    })
    scales.value = scaleresp
  } catch (error) {
    console.log(error.message)
    alert(error.message)
  }
})
</script>
<style scoped>
body {
  background-image: url('@/assets/BGimg1.jpg');
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: 100% 100%;
}
.jumbotron {
  font-family: cursive;
}
.container {
  display: flex;
  justify-content: center;
  padding-top: 100px;
}

.form-group {
  width: 50%;
  margin: 0 auto;
}
.form-group label {
  font-weight: bold;
}
</style>
