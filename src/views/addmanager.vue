<template>
  <navbar />
  <div id="m">
    <div class="container">
      <div class="jumbotron text-center">
        <h2>Add Store Manager</h2>
        <form @submit.prevent="signup" novalidate>
          <div class="form-group">
            <NameField v-model="user.name" />
          </div>
          <br />
          <div class="form-group">
            <EmailField v-model="user.email" />
          </div>
          <br />
          <div class="form-group">
            <PasswordField v-model="user.password" />
          </div>
          <br />
          <div class="form-group">
            <button
              class="btn btn-primary"
              @click="signUpButtonPressed"
              :disabled="isSignupButtonDisabled"
            >
              ADD
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
import EmailField from '@/components/EmailField.vue'
import PasswordField from '@/components/PasswordField.vue'
import customfetch from '../modules/customfetch'
import useFormValidation from '@/modules/useFormValidation'
import useSubmitButtonState from '@/modules/useSubmitButtonState'
import router from '../router'
const role = localStorage.getItem('user')
const loggedin = localStorage.getItem('loggedin')
onBeforeMount(() => {
  if (loggedin == 'true' && role != 'admin') {
    router.push('/')
  }
})

let user = reactive({
  name: '',
  email: '',
  password: ''
})
function signup() {
  customfetch('http://127.0.0.1:5000/ssignup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },

    body: JSON.stringify({ username: user.name, email: user.email, password: user.password })
  })
    .then((data) => {
      console.log(data)
      alert('Succesfully Registered, Redirecting to login page')
      localStorage.setItem('token', data.token)
      localStorage.setItem('loggedin', 'true')
      localStorage.setItem('username', 'storem')
      router.push('/slogin')
    })
    .catch((message) => {
      console.log(message)
      alert(message)
    })
}

const { errors } = useFormValidation()
const { isSignupButtonDisabled } = useSubmitButtonState(user, errors)

const signUpButtonPressed = () => {
  console.log(user)
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

#m {
  background-image: url('@/assets/BGimg3.jpg');
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: 100% 100%;
}
</style>
