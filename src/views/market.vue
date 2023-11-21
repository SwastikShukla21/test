<template>
  <div v-if="alertmessage.length!=0" :class="alertcat" style="text-align: center;">
    <!-- <span aria-hidden="true">&times;</span> -->
    <!-- <strong>Success!</strong> {{ message }} -->
    {{ alertmessage }}
  </div>
  <div class="jumobotron text-center">
    
    <div v-if="availableItems.length === 0">
      <p>No Products found. Add the products now!</p>
      <router-link class="btn btn-primary" :to="{ name: 'storem' }">Add Product</router-link>
    </div>
    <div v-else>
      <input v-model="search" type="text" placehlder="Search Products" />
      <button @click="searchproducts">Search</button>
      <br />
      <small><i>Note: Use "under" followed by price to search products under a price range.</i></small>
      <br />
      <small><i>Note: Use "over" followed by price to search products over a price range.</i></small>
      <div v-if="searched.length == 0 && search.length != 0"><h2>No Products found 🥲</h2></div>
      <div v-if="searched.length != 0">
        <h2>Search Results</h2>
        <div class="d-flex flex-row">
          <div v-for="product in searched" :key="product.id">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <h6 class="card-subtitle">₹{{ product.price }}/{{ product.ms }}</h6>
                <br />
                <p class="card-text text-wrap">{{ product.desc }}</p>
              </div>

              <div class="card-footer">
                <button
                  v-if="product.stock > 0"
                  @click="addItemToCart(product)"
                  class="btn btn-success"
                >
                  Add to Cart
                </button>
                <span v-else class="btn btn-danger">Out of Stock</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <h1>Available Products</h1>
      <br />
      <div style="text-align: right; padding-right: 10px">
        <button
          @click="
            () => {
              isCartOpen = true
            }
          "
          class="btn btn-primary btn-lg"
          style="text-align: right"
        >
          Cart ({{ cart.length }}) - ₹{{ cartTotal }}
        </button>
      </div>
      <br />
      <br />

      <div v-for="category in categories" :key="category.id">
        <div v-if="category.itemlen != 0">
          <div class="row border-dark">
            <h3 style="text-align: left">{{ category.name }}</h3>
          </div>
          <!-- <div class="column"> -->
          <div class="d-flex flex-row">
            <div v-for="product in getProductsInCategory(category.name)" :key="product.id">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title">{{ product.name }}</h5>

                  <h6  class="card-subtitle">Market Price :<s style="color:red">₹{{ marketprice(product.price) }}/{{ product.ms }}</s></h6>
                  <h6 class="card-subtitle">Our Price :₹{{ product.price }}/{{ product.ms }}</h6>
                  <br />
                  <p class="card-text text-wrap">{{ product.desc }}</p>
                </div>

                <div class="card-footer">
                  <button
                    v-if="product.stock > 0"
                    @click="addItemToCart(product)"
                    class="btn btn-success"
                  >
                    Add to Cart
                  </button>
                  <span v-else class="btn btn-danger">Out of Stock</span>
                </div>
              </div>
            </div>
          </div>
          <!-- </div> -->
        </div>
      </div>
    </div>
  </div>

  <div class="cart-modal" v-if="isCartOpen">
    <div class="cart-content">
      <h2>Cart</h2>

      <div v-for="cartItem in cart" :key="cartItem.id">
        <div class="card" style="width: 200px">
          <div class="card-body">
            <h5 class="card-title">{{ cartItem.name }}</h5>
            <h6 class="card-subtitle">₹{{ cartItem.price }}/{{ cartItem.ms }}</h6>
            <h6 class="card-subtitle">Quantity: {{ cartItem.quantity }}</h6>
          </div>
          <div class="card-footer">
            <div class="control">
              <button @click="increaseQuantity(cartItem)">+</button>
              <input
                v-model="cartItem.quantity"
                type="number"
                @input="
                  () => {
                    cartItem.quantity =
                      cartItem.quantity > cartItem.stock ? cartItem.stock : cartItem.quantity
                    cartItem.quantity = cartItem.quantity < 1 ? 1 : cartItem.quantity
                  }
                "
              />
              <button @click="decreaseQuantity(cartItem)">-</button>
            </div>
            <br />
            <button @click="removeItemFromCart(cartItem)" class="btn btn-danger btn-sm">
              Remove
            </button>
            <span v-if="cartItem.stock < 0">Out of Stock</span>
          </div>
        </div>
      </div>

      <div class="cart-summary">
        <h6 class="total-label">Total: ₹{{ cartTotal }}</h6>
        <button v-if="cart.length != 0" @click="placeorder" class="btn btn-primary">
          Place Order
        </button>
        <button
          @click="
            () => {
              isCartOpen = false
            }
          "
          class="btn btn-danger"
        >
          Close
        </button>
      </div>
    </div>
  </div>
  <!-- </div> -->
</template>

<script setup>
import { ref, computed, watch, onMounted,onBeforeMount} from 'vue'
import customfetch from '../modules/customfetch'
const loggedin = localStorage.getItem('loggedin')
import router from '../router/index'
onBeforeMount(()=>{
  if(loggedin!='true'){
    alert("Not logged in\nLogin to continue")
    router.push('/')
  }
})
onMounted(async () => {
  try {
    const categoriesresp = await customfetch('http://127.0.0.1:5000/categories', {
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      }
    })
    categories.value = categoriesresp
    const items = await customfetch('http://127.0.0.1:5000/getproducts', {
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': localStorage.getItem('token')
      }
    })
    availableItems.value = items
  } catch (error) {
    console.error('An error occurred:', error)
    alert(error.message)
  }
})

const availableItems = ref([])
const isCartOpen = ref(false)
const cart = ref([])
const categories = ref([])
const search = ref('')
const searched = ref([])

const alertmessage=ref("")
const alertcat=ref("")
const marketprice = (price) => {
  return price + price*0.10
}
const cartTotal = computed(() => {
  return cart.value.reduce((total, item) => total + item.price * item.quantity, 0)
})

const addItemToCart = (item) => {
  const existingItem = cart.value.find((cartItem) => cartItem.id === item.id)
  if (existingItem) {
    if (!isOutOfStock(existingItem)) {
      existingItem.quantity++
      showalert(item.name+" added to cart","success")
    }
  } else {
    if (!isOutOfStock(item)) {
      cart.value.push({ ...item, quantity: 1 })
      showalert(item.name+" added to cart","success")
    }
  }
}

const removeItemFromCart = (item) => {
  const index = cart.value.indexOf(item)
  if (index !== -1) {
    cart.value.splice(index, 1)
    showalert(item.name+" removed from cart","danger")
  }
}

const increaseQuantity = (item) => {
  if (!isOutOfStock(item)) {
    item.quantity++
  }
}
const isOutOfStock = (item) => {
  return item.quantity >= item.stock
}

const decreaseQuantity = (item) => {
  if (item.quantity > 1) {
    item.quantity--
  }
}
function searchproducts() {
  search.value = search.value.trim().toLowerCase()
  if (search.value.startsWith('under')) {
    searched.value = availableItems.value.filter(
      (product) => product.price < parseInt(search.value.split('under')[1])
    )
    console.log(searched.value)
  } else if (search.value.startsWith('over')) {
    console.log('over')
    searched.value = availableItems.value.filter(
      (product) => product.price > parseInt(search.value.split('over')[1])
    )
    console.log(searched.value)
  } else {
    searched.value = availableItems.value.filter((product) =>
      product.name.toLowerCase().startsWith(search.value)
    )

  
  }
  console.log(search.value)
}

function placeorder() {
  confirm('Are you sure you want to checkout?')
  customfetch('http://127.0.0.1:5000/checkout', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-access-token': localStorage.getItem('token')
    },
    body: JSON.stringify({
      cart: cart.value,
      total: cartTotal.value,
      username: localStorage.getItem('username')
    })
  })
    .then((data) => {
      if (data) {
        alert(data.message)
        cart.value = []
        cartTotal.value = 0
        isCartOpen.value = false
      }
    })
    .catch((error) => {
      console.error('An error occurred:', error)
      alert(error.message)
    })
}
const showalert = (message,alertcategory) => {
 
  alertmessage.value = message
  alertcat.value = "alert alert-"+alertcategory
  setTimeout(() => {
   
    alertmessage.value = ''
    alertcat.value=''
  }, 3000)
}

const getProductsInCategory = (name) => {
  return availableItems.value.filter((item) => item.category === name)
}

watch(cart, (newCart) => {
  console.log('Updated cart:', newCart)
})
</script>
<style>
.control {
  display: flex;
  align-items: center;
}
.control button {
  margin: 5 0px;
}
.control input {
  width: 50px;
  text-align: center;
}
.card {
  margin: 10px;
}
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
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
.jumbotron {
  font-family: cursive;
}
</style>
