<template>

    <div class="dashboard">
        <adminnav></adminnav>
        <div class="form">
        <h1>Create a Service</h1>
        <form class="form">
            <input type="text" placeholder="Name for Service" v-model="this.name"><br><br>
            <input type="text" placeholder="Description for Service" v-model="this.description"><br><br>
            <input type="number" placeholder="Base Price for the Service" v-model="this.price"><br><br>
            <input type="number" placeholder="Time Required for the service in hours" v-model="this.time_required"><br><br>
            <input type="number" placeholder="Professional(ID) to be assigned" v-model="this.prof_id"><br><br>
            <input type="file" @change="addFile"><br><br>
            <button type="button" id='submit' @click="addService">Add</button>
        </form>
    </div>
    </div>
</template>

<script>
import axios from 'axios';
import adminnav from '../components/adminnav.vue';
export default {
    name : 'addService',
    components :{
        adminnav
        
    },
    data(){
        return{
            name : null,
            description : null,
            price : null,
            time_required : null,
            token : null,
            message : null,
            img : null,
            prof_id : null
        }
    }, 
    created(){
        this.token = localStorage.getItem('authtoken')
        if(!this.token){
            this.$router.push('/login')
        }
    },
    methods:{
        addFile(e){
            this.img = e.target.files[0];
            console.log(this.img);
            

        },

        addService(){
            let formData = new FormData();
            formData.append('name', this.name)
            formData.append('description', this.description)
            formData.append('price', this.price)
            formData.append('time_required', this.time_required)
            formData.append('img', this.img) 
            formData.append('professional_id', this.prof_id)

            console.log([...formData]);
            
            axios
            .post('http://localhost:5002/api/service', formData,
                {headers : {Authorization: `${this.token}` },}


           )
           .then(response => {
            if(response.status == 201){
                this.message = response.data
                this.$router.push('/service')
            }
           })
           .catch(error =>{
                console.log(error);
                
           })
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
  height : 800px;
  background-image: url('@/assets/admin.jpg');
  background-position: center; 
  background-size: contain;
}

.form {
    max-width: 700px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #f9f9f9;

}
  

h1 {
    font-size: 1.8rem;
    color: #333;
    text-align: center;
    margin-bottom: 20px;
}

.form input[type="text"],
.form input[type="number"],
.form input[type="file"] {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

#submit {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

#button:hover {
    background-color: #0056b3;
}
</style>