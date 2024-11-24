<template>
    <custnav></custnav>
    <div >
        <h1>Edit Customer with id: {{ this.id }}</h1>
        <form>
            <input type="text" placeholder="Customer name" v-model="this.name"><br><br>
            <input type="text" placeholder="Customer city" v-model="this.city"><br><br>
            <input type="number" placeholder="Customer pincode" v-model="this.pincode"><br><br>
            <input type="number" placeholder="Customer Mobile no" v-model="this.mobileno"><br><br>
            <button type="button" id="submit" @click="edit()">Submit</button> 
            <button type="button" id="cancel" @click="cancel()"> Cancel</button>
        </form>
        {{ this.message }}
    </div>    
</template>

<script>
import axios from 'axios';
import custnav from '@/components/custnav.vue'
export default{
name: 'editcustomerprofile',
components:{
    custnav
},
data() {
   return{
    name: null,
    city: null,
    pincode: null,
    mobileno : null,
    token: null,
    message: null,
    id: localStorage.getItem('id')       
   } 
},
created(){
    this.token = localStorage.getItem('authtoken')
    if(!this.token){
        this.$router.push('/login')
    }
    this.GetCustomer()
},
methods: {
    
    edit(){
        axios
        .put(`http://localhost:5002/api/editcustomer/${this.id}`,
            {
                name: this.name,
                city: this.city,
                pincode : this.pincode,
                mobileno : this.mobileno,
            },
            {headers :{Authorization: `${this.token}` },}  
        )
        .then(response => {
            this.message = response.data.message
            if (response.status == 200){
               this.message = response.data,
               alert('Updated Successfully!')
               this.$router.push('/customerdashboard') 

            }                
        })
        .catch(error => {
            console.log(error);
        })
    },

    GetCustomer(){
        axios
        .get(`http://localhost:5002/api/getcustomer/${this.id}`,
        {headers :{Authorization: `${this.token}`},}  
        )
        .then(response => {
            if (response.status == 200){
               this.name = response.data.data.name,
               this.city = response.data.data.city,
               this.pincode = response.data.data.pincode,
               this.mobileno = response.data.data.mobno,
               console.log(response);

            
            
        }                
    })
        .catch(error => {
            console.log(error);
        })
  
    },

    cancel(){
        this.$router.push('/customerdashboard');
    }
}
}
</script>

<style scoped>
div {
    max-width: 400px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
h1 {
font-size: 1.5em;
color: #333;
text-align: center;
}
form {
display: flex;
flex-direction: column;
}
input, button {
margin: 8px 0;
padding: 10px;
font-size: 1em;
border: 1px solid #ccc;
border-radius: 4px;
}
#submit {
cursor: pointer;
background-color: #4CAF50;
color: white;
border: none;
}
#cancel {
background-color: #f44336;
}
button:hover {
opacity: 0.9;
}
p {
color: #4CAF50;
font-size: 1em;
text-align: center;
}
</style>
