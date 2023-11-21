<template>
  <div>
    <h2>Update Product</h2>
    <form @submit.prevent="updateProduct">
      <div class="form-group">
        <label for="name">Name:</label>
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
          step="0.01"
          required
        />
      </div>
      <div class="form-group">
        <label for="category">Category:</label>
        <select v-model="selectedCategory" class="form-control" id="category">
          <option v-for="category in categories" :key="category.id" :value="category.name">
            {{ category.name }}
          </option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary">Update Product</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeMount } from 'vue'
import customfetch from '../modules/customfetch'
import router from '../router/index'
import { useRoute } from 'vue-router'
const route = useRoute()
const name = ref('')
const quantity = ref(0)
const price = ref(0.0)
const selectedCategory = ref(null)
const categories = ref([])
const loggedin = localStorage.getItem('loggedin')
const user = localStorage.getItem('user')
onBeforeMount(() => {
  if (loggedin != 'true') {
    alert('Login to continue,')
    router.push('/slogin')
  } else if (loggedin == 'true') {
    if (user != 'storem') {
      alert('Unauthorized access!!!\nNot a store Manger Redirecting to Home page')
      router.push('/')
    }
  }
})
onMounted(async () => {
  try {
    const productId = route.params.id
    const productResponse = await customfetch(`http://127.0.0.1:5000/getproduct/${productId}`, {
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      }
    })


    name.value = productResponse.name
    quantity.value = productResponse.quantity
    price.value = productResponse.price
    selectedCategory.value = productResponse.category

    const categoriesresp = await customfetch('http://127.0.0.1:5000/categories', {
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      }
    })
    categories.value = categoriesresp
  } catch (error) {
    console.error('An error occurred:', error)
    alert(error.message)
  }
})

const updateProduct = async () => {
  try {
    const productId = route.params.id
    const response = await customfetch(`http://127.0.0.1:5000/updateproduct/${productId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      },
      body: JSON.stringify({
        name: name.value,
        quantity: quantity.value,
        price: price.value,
        category: selectedCategory.value
      })
    })
      .then((data) => {
        if (data) {
          alert('Product updated successfully')
          router.push('/products')
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
