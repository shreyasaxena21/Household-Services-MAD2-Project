<template>
   <pronav></pronav>
    <div >
        <h1>Edit Customer with id: {{ this.id }}</h1>
        <form>
            <input type="text" placeholder="Professional name" v-model="this.name"><br><br>
            <input type="text" placeholder="Professional Service Type" v-model="this.service_type"><br><br>
            <input type="number" placeholder="Professional experience" v-model="this.experience"><br><br>
            <button type="button" id="submit" @click="edit()">Submit</button> 
            <button type="button" id="cancel" @click="cancel()"> Cancel</button>
        </form>
        {{ this.message }}
    </div>    
</template>

<script>
import axios from 'axios';
import pronav from '@/components/pronav.vue'
export default{
name: 'editprofessionalprofile',
components:{
    pronav
},
data() {
   return{
    name: null,
    service_type: null,
    experience: null,
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
    this.GetProfessional()
},
methods: {
    edit(){
        axios
        .put(`http://localhost:5002/api/editprofessional/${this.id}`,
            {
                name: this.name,
                service_type: this.service_type,
                experience : this.experience,
            },
            {headers :{Authorization: `${this.token}` },}  
        )
        .then(response => {
            this.message = response.data.message
            if (response.status == 200){
               this.message = response.data,
               alert('Updated Successfully!')
               this.$router.push('/professionaldashboard') 

            }                
        })
        .catch(error => {
            console.log(error);
        })
    },

    GetProfessional(){
        axios
        .get(`http://localhost:5002/api/getprofessional/${this.id}`,
        {headers :{Authorization: `${this.token}`},}  
        )
        .then(response => {
            if (response.status == 200){
               this.name = response.data.data.name,
               this.service_type = response.data.data.service_type,
               this.experience = response.data.data.experience
               console.log(response);

            
            
        }                
    })
        .catch(error => {
            console.log(error);
        })
  
    },

    cancel(){
        this.$router.push('/professionaldashboard');
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
