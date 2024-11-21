<template>
  <div class='panel'>
      <homenav></homenav>
        <div class="container">

          <h1>User Login</h1>
          <form>
            <div class="form-group">
                <label for="exampleInputEmail1">Email </label>
                <input type="email" class="form-control" id="exampleInputEmail1" name="email" v-model="this.email" aria-describedby="emailHelp" placeholder="Enter email"><br>
            </div>
            <div class="form-group">
                <label for="exampleInputPassword1">Password </label>
                <input type="password" class="form-control" id="exampleInputPassword1" name="password" v-model="this.password" placeholder="Password">
            </div><br>
            <button type="button" @click="login_fn" class="btn btn-success">Login</button>
            </form><br>

            <!-- Error Message -->
          <div v-if="errorMessage" id="error-message">
            {{ errorMessage }}
          </div>

        </div>
      </div>
</template>

<script>
import axios from 'axios';
import homenav from '../components/homenav.vue'

export default {
  name: "login",
  components:{
     homenav
  },
  data() {
      return{
          email : "",
          password : "",
          errorMessage : null,
         
      }
  },
  methods: {
      login_fn() {
          console.log("User email :" + this.email);
          console.log("User password :" + this.password);
          axios
          .post("http://localhost:5002/api/login", {
              email : this.email,
              password : this.password
          })
          .then(response => {
              console.log(response.data.message);
              console.log(response);
              
              if(response.status == 200){
                  localStorage.setItem('authtoken', response.data.token)
                  localStorage.setItem('id', response.data.id)
                  localStorage.setItem('email', response.data.email)
                  localStorage.setItem('role', response.data.role)
                  localStorage.setItem('name', response.data.name)

                  this.role = response.data.role;
              }
              
          })
          .catch(error => {
              console.log('catched error :' +error)
              this.errorMessage = error.response?.data?.message
              console.log(this.errorMessage);
              
          })
          .finally(() => {
            switch (this.role) {
                  case 'admin':
                      this.$router.push('/admindashboard');
                      break;
                  case 'service_professional':
                      this.$router.push('/professionaldashboard');
                      break;
                  case 'customer':
                      this.$router.push('/customerdashboard');
                      break;
                  default:
                      this.$router.push('/login');
            }

          })
          
      }
  }
}
</script>

<style scoped>

.panel{
  height: 750px;
  background-image: url('https://cdn.vectorstock.com/i/500p/53/49/cleaning-house-doodles-vector-1445349.jpg');
}

.container {
  max-width: 400px;
  margin: 150px auto;
  padding: 20px;
  border: 2px solid #1b0534;
  border-radius: 10px;
  text-align: center;
  background-color: rgba(255, 255, 255, 0.85); /* Slightly transparent white background */
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2); /* Add shadow for a lifted effect */
  position: relative;
  z-index: 10;
  background-color:white;
}



/* Heading styling */
h2 {
  margin-bottom: 20px;
}

/* Form styling */
form {
  display: flex;
  flex-direction: column;
}

input,
select {
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

#error-message{
  color: red;
}
</style>
