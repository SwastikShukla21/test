<template>
  <router-view></router-view>

  <div id="m">
    <div class="container">
      <div class="jumbotron text-center">
        <h1>Get Ready for Shopping</h1>
        <h5>Enter your details</h5>
        <form @submit.prevent="login" novalidate>
          <NameField v-model="user.name" />

          <br />

          <PasswordField v-model="user.password" />
          <br />
          <div class="form-group">
            <button
              class="btn btn-primary"
              :disabled="isSignupButtonDisabled"
              @click="loginButtonPressed"
            >
              LOG IN
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onBeforeMount } from 'vue'
import NameField from '@/components/NameField.vue'
import PasswordField from '@/components/PasswordField.vue'
import useFormValidation from '../modules/useFormValidation'
import useSubmitButtonState from '../modules/useSubmitButtonState'

import customfetch from '../modules/customfetch'
import router from '../router/index'
const loggedin = localStorage.getItem('loggedin')
const role = localStorage.getItem('user')
const user = reactive({
  name: '',
  password: ''
})
onBeforeMount(() => {
  if (loggedin == 'true' && role == 'customer') {
    router.push('/market')
  }
})

function login() {
  customfetch('http://127.0.0.1:5000/clogin', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },

    body: JSON.stringify({ username: user.name, password: user.password })
  })
    .then((data) => {
      console.log(data.token)
      localStorage.setItem('token', data.token)
      localStorage.setItem('user', 'customer')
      localStorage.setItem('loggedin', 'true')
      localStorage.setItem('username', data.username)
      router.push('/market')
    })
    .catch((err) => {
      console.log(err.message)
      alert(err.message)
    })
}

const { errors } = useFormValidation()
const { isSignupButtonDisabled } = useSubmitButtonState(user, errors)

const loginButtonPressed = () => {
  console.log(user)
}
</script>

<style>
.jumbotron {
  /* background-image: url("@/assets/BGimg3.jpg"); */
  font-family: cursive;
}
.container {
  display: flex;
  justify-content: center;
  padding-top: 100px;
}

#m {
  background-image: url('@/assets/BGimg3.jpg');
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: 100% 100%;
}
</style>
