<template>
    
    <div class="container-lg" id="main">
            <br>
            <h1>Admin Panel</h1>
            <br>
            <div class="jumbotron text">
               
                
                <!-- <img src="/static/pic3.png"> -->
                <div class="row">
                    <div class="col-md-6">
                    <div class="container-md" id="child">
                        <br>
                        <h3>Add a Category</h3>
                        <br>
                        <br>
                        <button class="btn btn-primary" @click="addsection">ADD</button>
                        

                    </div>
                    </div>
                    <div class="col-md-6">
                        <div class="container-md" id="child">
                            <br>
                            <h3> Show Categories </h3>
                            <br>
                            <br>
                            
                            <button class="btn btn-primary" @click="sections">VIEW</button>
                        </div>
                        </div>
                    </div>
                        
                        
                        
                            <br>
                        <div class="row ">
                            <div class="col-md-6">
                                <div class="container-md" id="child">
                                    <br>
                                    <h3>Show Products</h3>
                                    <br>
                                    <br>
                                    <button class="btn btn-primary" @click="showproducts">VIEW</button>

                                    
                                </div>
                                </div>
                        
                            <div class="col-md-6">
                                <div class="container-md" id="child">
                                    <br>
                                    <h3>Show Requests</h3>
                                    <br>
                                    <br>
                                    <button class="btn btn-primary" @click="requests">VIEW</button>

                                    
                                </div>
                                </div>
                        </div>
                        <br>
                    
                </div>
                
                    
                  
                </div>
        
</template>
<script >
import {ref} from 'vue'
import router from '../router/index'
import customfetch from "../modules/customfetch"
export default{
    
    setup(){
        function addsection(){
            router.push('/addsection')
        }
        function sections(){
            router.push('/categories')
        }
        
        function requests(){
            router.push('/adminrequests')
        }
        function showproducts(){
            router.push('/products')
        }
        return{
            addsection,
            sections,
            requests,
            showproducts
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
        #main{
            background-color:rgb(255, 255, 100);
            font-family:cursive;
            text-align: center;
        }
        #child{
            background-color:lightyellow;
            font-family: Georgia, 'Times New Roman', Times, serif;
            text-align: left;

        }

</style>