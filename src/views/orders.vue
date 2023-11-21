<!-- a page for showing orders use a table to display the orders -->
<template>
  <h1 style="text-align: center">Your Orders</h1>
  <div class="container">
    <div class="jumbotron">
      <div v-if="!orders.length">
        <h2>No Orders to show</h2>
        <router-link to="/market">
          <button class="btn btn-primary">Shop on EMarket</button>
        </router-link>
      </div>

      <div v-else>
        <table>
          <thead>
            <tr id="top">
              <th>Order Id</th>
              <th>
                <div v-if="role == 'storem'">Customer Name</div>
              </th>
              <th>Order Value</th>
              <th>Order Date</th>
              <th>Order Time</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orders" :key="order.order_id">
              <!-- <td>{{order.id}}</td> -->

              <td style="color: green">
                <a @click="showorderdetails(order.id)"
                  ><u>{{ order.id }}</u></a
                >
              </td>
              <td>
                <div v-if="role == 'storem'">
                  {{ order.name }}
                </div>
              </td>

              <td>₹{{ order.order_value }}</td>
              <td>{{ order.order_date }}</td>
              <td>{{ order.order_time }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- describe a modal to show the order details -->
    </div>
  </div>
  <div class="cart-modal" v-if="isorderdetails">
    <div class="cart-content">
      <h2>Order Details</h2>
      <table>
        <thead>
          <tr id="top">
            <th>Product Name</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="transaction in transactions" :key="transaction.id">
            <td>{{ transaction.name }}</td>
            <td>{{ transaction.quantity }}</td>
            <td>{{ transaction.price }}</td>
            <td>{{ transaction.quantity }} x {{ transaction.price }} = ₹{{ transaction.value }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <button
      @click="
        () => {
          isorderdetails = false
          transactions = []
        }
      "
      class="btn btn-danger"
    >
      Close
    </button>
  </div>
</template>
<script setup>
import { ref, onMounted, onBeforeMount } from 'vue'
import customfetch from '../modules/customfetch'
import router from '../router/index'

const orders = ref([])
const transactions = ref([])
const isorderdetails = ref(false)

const loggedin = localStorage.getItem('loggedin')
const role = localStorage.getItem('user')
onBeforeMount(() => {
  if (loggedin != 'true') {
    alert('Not logged in\nRedirecting to Homepage')
    router.push('/')
  }
})

function showorderdetails(id) {
  isorderdetails.value = true
  const response = customfetch('http://localhost:5000/gettransaction', {
    headers: {
      'Content-Type': 'application/json',
      'x-access-token': localStorage.getItem('token'),
      orderid: id
    }
  }).then((data) => {
    transactions.value = data
  })
}
onMounted(async () => {
  try {
    const response = await customfetch('http://127.0.0.1:5000/getorders', {
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token'),
        username: localStorage.getItem('username'),
        user: localStorage.getItem('user')
      }
    })
    orders.value = response
  } catch (error) {
    console.log(error.message)
    alert(error.message)
  }
})
</script>
<style>
.cart-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* background-color: rgba(0, 0, 0, 0.5); */
  display: flex;
  align-items: center;
  justify-content: center;
}
.cart-content {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  background-color: white;
  padding: 20px;
  border-radius: 10px;
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
  text-align: center;
}
table {
  display: block;
  border-spacing: 10px;
  border: 2px solid black;
}
#top {
  border-top: 1px solid black;
}
.jumbotron {
  background-color: rgb(255, 255, 100);
  font-family: cursive;
}
.container {
  display: flex;
  justify-content: center;
  padding-top: 100px;
}
</style>
