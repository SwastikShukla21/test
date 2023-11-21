<template>
    <div>
        <div class="container">
          
        <div class="jumbotron text-center">
          <input v-model="search" type="text" placeholder=" Search Products by name" />
          <button @click="searchproducts">Search</button>
          <br>
          <small><i>Note:Use "under" followed by price to serach products under a price range </i></small>
          <div v-if="searched.length==0 && search.length!=0">No products found</div>
          <div v-if="searched.length!=0" >
          <h2>Search Results</h2>
          
          
          <table>
          <thead>
            <tr id="top">
              <th>Product Name</th>
              <th>Quantity</th>
              <th>Price</th>
              <th>Category</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in searched" :key="product.id">
              <td>{{ product.name }}</td>
              <td>{{ product.quantity }}</td>
              <td>{{ product.price }}</td>
                <td>{{ product.category }}</td>
              <td>
                <button @click="editProduct(product.id)" class="btn btn-primary">Edit</button>
                <button @click="deleteProduct(product.id)" class="btn btn-danger">Delete</button>
              </td>
            </tr>
          </tbody>
          </table>
          </div>

          
      <h2>Product List</h2>
      <div v-if="products.length===0">
        <p>No Products found. Add the products now!</p>
        <router-link class="btn btn-primary" :to="{ name: 'addproduct' }">Add Product</router-link>
      </div>
      <div v-else>
        <table>
          <thead>
            <tr id="top">
              <th>Product Name</th>
              <th>Quantity</th>
              <th>Price</th>
              <th>Category</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product.id">
              <td>{{ product.name }}</td>
              <td>{{ product.stock }}</td>
              <td>{{ product.price }}</td>
                <td>{{ product.category }}</td>
              <td>
                <button @click="editProduct(product.id)" class="btn btn-primary">Edit</button>
                <button @click="deleteProduct(product.id)" class="btn btn-danger">Delete</button>
              </td>
            </tr>
          </tbody>
          <button @click="exportproducts" class="btn btn-primary">Export as CSV</button>
          <div v-if="exporting" >Exporting....</div>
          <a v-if="csvlink" :href="csvlink" download @click="resetdownoladlink">Download</a> 
        
          </table>
      </div>
        </div>
    </div>
        
      
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted,onBeforeMount } from 'vue';
  import router from '../router/index';
  import customfetch from '../modules/customfetch';
  
  const products = ref([]);
  const exporting=ref(false);
  const csvlink=ref(null);
  const search=ref("")
  const searched=ref([])
  const loggedin = localStorage.getItem('loggedin')

onBeforeMount(() => {
  if (loggedin!='true') {
    alert('Unauthorized Access\nRedirectiong to Home Page')
    router.push('/')
  } 
})
  onMounted(async () => {
    try {
      const response = await customfetch('http://127.0.0.1:5000/getproducts', {
        headers: {
          'Content-Type': 'application/json',
          'x-access-token': localStorage.getItem('token')
        }
      });
      products.value = response;

  } catch (error) {
      console.log( error.message)
      alert(error.message)
    }
}
);
  function searchproducts() { console.log(search.value)
    search.value=search.value.trim()
    search.value=search.value.toLowerCase()
    if (search.value.startsWith("under")){
      console.log("under")
      searched.value=products.value.filter((product)=>  product.price<parseInt(search.value.split("under")[1]))
      console.log(searched.value)
    
    }
    else if(search.value.startsWith("over"))
    {
      console.log("over")
      searched.value=products.value.filter((product)=>  product.price>parseInt(search.value.split("over")[1]))
      console.log(searched.value)
    }
    else{
    searched.value=products.value.filter((product)=>  product.name.toLowerCase().startsWith(search.value))
    
    console.log(searched.value)
    }
  } 
  console.log(search.value)
  const editProduct = (productId) => {
    router.push(`/updateproduct/${productId}`);
  };
  async function exportproducts(){
    exporting.value=true;
    try{
      const response = await customfetch('http://127.0.0.1:5000/exportproducts', {
        headers: {
          'Content-Type': 'application/json',
          'x-access-token': localStorage.getItem('token')
        }
      });
    if (response.task_id){
      checkstatus(response.task_id);

    }else{
      console.error('Task ID absent')
    }
  }catch(error){
    console.error('An error occured while exporting')
    alert('An error occured while exporting')

  }
  exporting.value=false;
}
async function checkstatus(taskid){
  try{
    const response=await customfetch(`http://127.0.0.1:5000/checkstatus/${taskid}`,{
      method:'GET',
      headers:{
        'Content-Type':'application/json',
        'x-access-token':localStorage.getItem('token')
      }

    });
    if (response.status==='success'){
      csvlink.value=response.csvlink
      alert('Export Completed');
    }else if(response.status==='pending'){
      setTimeout(()=>{ checkstatus(taskid);},2000);
    }
  }
  catch(error){
    console.error('An error occurred while checking status')
  }
}
function resetdownoladlink(){ csvlink.value=null

}
    
    
  
  async function deleteProduct(productId) {
if (confirm('Are you sure you want to delete this product?')) {
try {
const response = await customfetch(`http://127.0.0.1:5000/deleteproduct/${productId}`, {
method: 'GET',
headers: {
'Content-Type': 'application/json',
'x-access-token': localStorage.getItem('token')
}
}).then((data)=>{
  if(data){
    alert("Product deleted successfully")
    router.push("/storempanel")
  }
}).catch((err)=>{console.log(err)
  alert(err.message)})
} catch (error) {
console.error('An error occurred:', error);
}
}
}
  </script>
  <style>
    .jumbotron{
            background-color:rgb(255, 255, 100);
            font-family:cursive;
            
            
            

        }
        .container{
            display: flex;
            justify-content: center;
            padding-top:100px;
        }
        .p a{
            color:green;
        }
        tr {
            border-bottom: 1px solid black;
        }
        th{ text-align: center;
            padding:10px;
        }
        td{
            padding: 10px;
        }
        table{
            display:block;
            border-spacing: 10px;
            border: 2px solid black;
        }
        #top{
            border-top:1px solid black;
        }

  </style>
  