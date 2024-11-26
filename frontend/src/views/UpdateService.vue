<template>
    <div class="dashboard">
        <adminnav></adminnav>
        <div class="form">
            <h1>Edit a Service with id: {{ this.id }}</h1>
            <form>
                <input type="text" placeholder="name for the service" v-model="this.name"><br><br>
                <input type="text" placeholder="description for the category" v-model="this.description"><br><br>
                <input type="number" placeholder="Base Price for the Service" v-model="this.price"><br><br>
                <input type="number" placeholder="Time Required for the service in hours" v-model="this.time_required"><br><br>
                <button type="button" id="submit" @click="addService()">Submit</button> 
                <button type="button" id="cancel" @click="cancel()"> Cancel</button>
            </form>
            {{ this.message }}
        </div>
    </div>    
</template>

<script>
import axios from 'axios';
import adminnav from '@/components/adminnav.vue'
export default{
    name: 'updateService',
    components:{
        adminnav
    },
    data() {
       return{
        name: null,
        description: null,
        price: null,
        time_required : null,
        token: null,
        message: null,
        id: null        
       } 
    },
    created(){
        this.id = this.$route.params.id;
        this.token = localStorage.getItem('authtoken')
        if(!this.token){
            this.$router.push('/login')
        }
        this.fetchService()
    },
    methods: {
        addService(){
            axios
            .put(`http://localhost:5002/api/service/${this.id}`,
                {
                    name: this.name,
                    description: this.description,
                    price : this.price,
                    time_required : this.time_required,
                },
                {headers :{Authorization: `${this.token}` },}  
            )
            .then(response => {
                this.message = response.data.message
                if (response.status == 201){
                   this.message = response.data,
                   this.$router.push('/admindashboard') 
                }                
            })
            .catch(error => {
                console.log(error);
            })
        },

        
        fetchService(){
            axios
            .get(`http://localhost:5002/api/service/${this.id}`,
            {headers :{Authorization: `${this.token}`},}  
            )
            .then(response => {
                if (response.status == 200){
                   this.name = response.data.data.name,
                   this.description = response.data.data.description,
                   this.price = response.data.data.price,
                   this.time_required = response.data.data.time_required,
                   console.log(response);
                   console.log('Service: ' +this.service);
                
                
            }                
        })
            .catch(error => {
                console.log(error);
            })
      
        },

        cancel(){
            this.$router.push('/admindashboard');
        }
    }
}
</script>

<style scoped>
.dashboard {
  text-align: center;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  height : 730px;
  background-image: url('@/assets/customer.jpg');
  background-position: center; 
  background-size: contain;
}

.form {
    max-width: 400px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #f9f9f9;

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
