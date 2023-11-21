<template>
  <div class="container-lg" id="main">
    <br />
    <h1>Inventory Management</h1>
    <div class="jumbotron text">
      <!-- <img src="/static/pic3.png"> -->
      <div class="row">
        <div class="col-md-6">
          <div class="container-md" id="child">
            <br />
            <h3>Add a Product</h3>
            <br />
            <br />
            <button class="btn btn-primary" @click="addproduct">ADD</button>
          </div>
        </div>
        <div class="col-md-6">
          <div class="container-md" id="child">
            <br />
            <h3>Show Products</h3>
            <br />
            <br />

            <button class="btn btn-primary" @click="products">SHOW</button>
          </div>
        </div>
      </div>

      <br />
      <div class="row">
        <div class="col-md-6">
          <div class="container-md" id="child">
            <br />
            <h3>View or Make Requests</h3>
            <br />
            <br />
            <button class="btn btn-primary" @click="requests">VIEW</button>
          </div>
        </div>
          <div class="col-md-6">
            <div class="container-md" id="child">
              <br />
              <h3>Summary</h3>
              <br />
              <br />
              <button class="btn btn-primary" @click="summary">VIEW</button>
            </div>
          </div>
        </div>
        <br />
      </div>
    </div>

</template>
<script setup>
import { ref,onBeforeMount} from 'vue'
import router from '../router/index'
const loggedin = localStorage.getItem('loggedin')
const user = localStorage.getItem('user')
onBeforeMount(() => {
  if (loggedin!='true') {
    alert('Login to continue,')
    router.push('/slogin')
  } else if (loggedin=='true' && user!='storem') {
    
      alert('Unauthorized access!!!\nNot a store Manger Redirecting to Home page')
      router.push('/')
    
  }
})

    function addproduct() {
      router.push('/addproduct')
    }
    function products() {
      router.push('/products')
    }

    function requests() {
      router.push('/storemrequest')
    }
    
    function summary() {
      router.push('/summary')
    }
</script >
<style scpoed>
.jumbotron {
  background-color: rgb(255, 255, 100);
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
#main {
  background-color: rgb(255, 255, 100);
  font-family: cursive;
  text-align: center;
}
#child {
  background-color: lightyellow;
  font-family: Georgia, 'Times New Roman', Times, serif;
  text-align: left;
}
</style>
