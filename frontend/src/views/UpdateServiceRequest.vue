<template>
    <div class="dashboard">
    <custnav></custnav>
    <div class="form">
        <h1>Edit a Service Request with id: {{ this.id }}</h1>
        <form>
            <input type="text" placeholder="Date of Completion" v-model="this.date_of_completion"><br><br>
            <input type="text" placeholder="Status (Completed ?)" v-model="this.service_status"><br><br>
            <input type="text" placeholder="Remarks for the professional" v-model="this.remarks"><br><br>
            <button type="button" id="submit" @click="addServiceRequest">Submit</button> 
            <button type="button" id="cancel" @click="cancel"> Cancel</button>
        </form>
        {{ this.message }}
    </div>  
</div>  
</template>


<script>
import axios from 'axios';
import custnav from '../components/custnav.vue'
export default{
    name: 'updateservicerequest',
    components : {custnav},
    data() {
       return{
        date_of_completion: null,
        service_status: null,
        remarks: null,
        token: null,
        message: null,
        id: null        
       } 
    },
    created(){
        this.id = this.$route.params.id;
        console.log("Service Request ID:", this.id); 
        this.token = localStorage.getItem('authtoken')
        if(!this.token){
            this.$router.push('/login')
        }
        this.fetchServiceRequest()
    },
    methods: {
        addServiceRequest(){
            axios
            .put(`http://localhost:5002/api/servicerequest/${this.id}`,
                {
                    date_of_completion: this.date_of_completion,
                    service_status: this.service_status,
                    remarks : this.remarks,
                },
                {headers :{Authorization: `${this.token}` },}  
            )
            .then(response => {
                this.message = response.data.message
                if (response.status == 200){
                   this.message = response.data,
                   alert("Updated Successfully!")
                   this.$router.push('/customerdashboard') 
                }                
            })
            .catch(error => {
                console.log(error);
            })
        },

        fetchServiceRequest(){
            axios
            .get(`http://localhost:5002/api/getservicerequest/${this.id}`,
            {headers :{Authorization: `${this.token}`},}  
            )
            .then(response => {
                if (response.status == 200){
                   this.date_of_completion = response.data.data.date_of_completion,
                   this.service_status = response.data.data.service_status,
                   this.remarks = response.data.data.remarks,
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

