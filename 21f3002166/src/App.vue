<template>
  <navbar />
  <body>
    <router-view></router-view>
  </body>
  
  

  
  
</template>
<script>
import { RouterLink, RouterView } from 'vue-router'
import {ref} from 'vue'
import navbar from "@/components/navbar.vue"
import { useRoute, useRouter } from 'vue-router';

export default {
  name: 'App',
  components: {
    navbar,
    RouterLink,
    RouterView,
  
  },

  
  
}

</script>


<style>
#app{
  margin:0;
  padding:0;
  background-color: rgb(255, 255, 100);
  
  flex-direction: column;
  justify-content: center;
}
body{
  margin:0;
  padding: 0;
  background-size:100% 100%;
  background-attachment:fixed;
  background-repeat:no-repeat;
  background-image: url("@/assets/BGimg3.jpg")
}
</style>

