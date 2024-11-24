<template>
  <div class="panel">
    <homenav></homenav>
    <div class="container" >
      <h2>Register as a</h2>
      <label for="role">Select Role : </label>
      <select v-model="role" @change="handleRoleChange">
        <option value="" disabled>Select a role</option>
        <option value="customer">Customer</option>
        <option value="service_professional">Service Professional</option>
      </select>

      <div v-if="role === 'customer'">
        <h3>Customer Registration</h3>
        <form @submit.prevent="submitCustomerForm">
          <input type="text" v-model="customerData.name" placeholder="Name" required />
          <input type="text" v-model="email" placeholder="Email" required />
          <input type="password" v-model="password" placeholder="Password" required />
          <input type="text" v-model="customerData.city" placeholder="City" required />
          <input type="text" v-model="customerData.pincode" placeholder="Pincode" required />
          <input type="text" v-model="customerData.mobileNo" placeholder="Mobile No" required />
          <button type="button" @click="register_fn">Register</button>
        </form>
      </div>

      <div v-else-if="role === 'service_professional'">
        <h3>Service Professional Registration</h3>
        <form @submit.prevent="submitServiceProfessionalForm">
          <input type="text" v-model="service_professionalData.name" placeholder="Name" required />
          <input type="text" v-model="email" placeholder="Email" required />
          <input type="password" v-model="password" placeholder="Password" required />
          <input type="text" v-model="service_professionalData.experience" placeholder="Experience" required />
          <input type="text" v-model="service_professionalData.serviceType" placeholder="Service Type" required />
          <input type="text" v-model="service_professionalData.description" placeholder="Description" required />
          <!-- <input type="file" @change="addFile"> -->


          <button type="button" @click="register_fn">Register</button>
        </form>
      </div>
    </div>
 </div>
</template>
<script>
import axios from 'axios';
import homenav from '../components/homenav.vue'

export default {
  name: 'register',
  components:{
     homenav
  },
  data() {
    return {
      role: null,
      email : null,
      password : null,
     
      customerData: {
        name: null,
        city: null,
        pincode: null ,
        mobileNo: null
      },
      service_professionalData: {
        name: null ,
        experience: null ,
        serviceType: null ,
        description: null ,
        // image : null
      }
    };
  },

  methods: {
    // addFile(e){
    //     this.service_professionalData.image = e.target.files[0];
    //     console.log(this.service_professionalData.image);
        

    // },

    register_fn() {
        let formData = new FormData();
        formData.append('email', this.email)
        formData.append('password', this.password)
        formData.append('role', this.role)
       
        if (this.role === "customer") {
          formData.append('name', this.customerData.name)
          formData.append('city', this.customerData.city)
          formData.append('pincode', this.customerData.pincode)
          formData.append('mobileNo', this.customerData.mobileNo)
        
        } else if (this.role === "service_professional") {
            formData.append('name', this.service_professionalData.name)
            formData.append('experience', this.service_professionalData.experience)
            formData.append('serviceType', this.service_professionalData.serviceType)
            formData.append('description', this.service_professionalData.description)
            formData.append('documents', this.service_professionalData.documents)
            // formData.append('image', this.service_professionalData.image)
      
        }

        axios
          .post("http://localhost:5002/api/register", formData)
          .then((response) => {
            console.log(response.data.message);
            if (response.status == 201) {
              this.$router.push("/login");
            }
          })
          .catch((error) => {
            console.log("Caught error: " + error);
          });
      }
      }
      }

</script>

<style scoped>

.panel{
  height: 750px;
  background-image: url('https://png.pngtree.com/background/20230615/original/pngtree-cleaning-tools-and-cleaning-supplies-on-table-under-wooden-fence-picture-image_3543018.jpg');
  background-position: center; 
  background-size: contain;
  background-repeat: no-repeat;
  background-color: rgb(230, 235, 238);
}
.container {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
  background-color: #f9f9f9;
}


h2 {
  margin-bottom: 20px;
}

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
  background-color: #0d9b24;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #00b306;
}
</style>