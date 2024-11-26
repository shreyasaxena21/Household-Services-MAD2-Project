<template>
  
      <div class="dashboard">
        <custnav></custnav>
        <h3>Welcome {{ this.name }}</h3>
        
  

        <h3 style="font-family: Georgia, 'Times New Roman', Times, serif;">List of active Service Professionals</h3>
          <table class="service-table">
            <thead>
              <tr>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Id</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Name</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Email</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Service Type</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Location</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Experience</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Actions</th>

              </tr>
            </thead>
            <tbody>
              <tr v-for="active in active_prof" :key="active.id">
                <td>{{ active.id }}</td>
                <td>{{ active.name }}</td>
                <td>{{ active.email }}</td>
                <td>{{ active.service_type }}</td>
                <td>{{ active.location }}</td>
                <td>{{ active.experience }}</td>
                <td>
                  <input type="text" v-model="active.message" placeholder="Enter details" style="margin-right: 8px; padding: 4px; border: 1px solid #ccc; border-radius: 4px;"/>
                  <input type="date" v-model="active.date_of_completion" placeholder="Date of Completion" style="margin-right: 8px; padding: 4px; border: 1px solid #ccc; border-radius: 4px;"/>
                  <button @click="createServiceRequest(active.id, active.message, active.date_of_completion, active.service_type)" style="background-color: #2ecc71; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer;">Book</button>
                </td>

                
              </tr>
            </tbody>
          </table>

          <h3 style="font-family: Georgia, 'Times New Roman', Times, serif;">Service Requests</h3>
          <table class="service-table">
            <thead>
              <tr>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Id</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Professional Name</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Service Name</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Date of Request</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Message</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Status</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Date of Completion</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Actions</th>

              </tr>
            </thead>
            <tbody>
              <tr v-for="request in service_request" :key="request.id">
                <td>{{ request.id }}</td>
                <td>{{ request.prof_name }}</td>
                <td>{{ request.service_name }}</td>
                <td>{{ request.date_of_request }}</td>
                <td>{{ request.message }}</td>
                <td>{{ request.service_status }}</td>
                <td>{{ request.date_of_completion }}</td>
                <td>
                  <router-link :to="{ name: 'updateservicerequest', params: { id: request.id } }" class="btn btn-update">Edit Request</router-link> 
                  <router-link :to="{ name: 'closeservicerequest', params: { id: request.id } }" id="close">Close Request</router-link> 
                </td>
              </tr>
            </tbody>
          </table>

          <h3 style="font-family: Georgia, 'Times New Roman', Times, serif;">Past Service Requests</h3>
          <table class="service-table">
            <thead>
              <tr>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Id</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Professional Name</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Service Name</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Date of Request</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Remarks</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Status</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Date of Completion</th>

              </tr>
            </thead>
            <tbody>
              <tr v-for="request in completed_service_request" :key="request.id">
                <td>{{ request.id }}</td>
                <td>{{ request.prof_name }}</td>
                <td>{{ request.service_name }}</td>
                <td>{{ request.date_of_request }}</td>
                <td>{{ request.remarks }}</td>
                <td>{{ request.service_status }}</td>
                <td>{{ request.date_of_completion }}</td>
              </tr>
            </tbody>
          </table>
        </div>
  </template>
  
<script>
import custnav from '../components/custnav.vue'
import addservicerequest from './UpdateServiceRequest.vue'
import axios from 'axios';
export default{
    name : "customerdashboard",
    components: {
      addservicerequest,
      custnav
    },
    data() {
      return {
        customer_id : localStorage.getItem('id'),
        token: null,
        message: null,
        date_of_completion: null,
        service: [],
        service_id: null,
        active_prof : [],
        active_prof_id : null,
        service_request : [],
        service_request_id : null,
        completed_service_request : [],
        completed_service_request_id : null,
        name : localStorage.getItem('name')
      };
    },
    created() {
      this.token = localStorage.getItem('authtoken');
      if (!this.token) {
        this.$router.push('/login');
      } else {
        this.fetchActiveProfessional();
        this.fetchService()
        this.fetchServiceRequests();
        this.fetchCompletedRequests();
      }
    },
    methods: {
      createServiceRequest(professionalId, message, date_of_completion, service_type) {
        console.log('Customer ID:', this.customer_id);
        console.log('Service Type:', service_type);
        console.log('Professional ID:', professionalId);
        console.log('Message:', message);
        console.log('Date of Completion:', date_of_completion);  
        // console.log(`Booking professional with ID: ${professionalId}, Message: ${message}, date_of_completion : ${date_of_completion}`);
          axios
          .post('http://localhost:5002/api/createservicerequest', 
            {
              professional_id: professionalId,
              message: message,
              date_of_completion : date_of_completion,
              service_type : service_type,
              customer_id : this.customer_id
            },
            {
              headers: { Authorization: `${this.token}` },
            }
          )
          .then(response => {
            if (response.status === 201) {
              console.log(response.data);
              alert("Service booked successfully!");
              location.reload();
            }
          })
          .catch(error => {
            console.error("Error booking service:", error);
          });
        },



      fetchActiveProfessional(){
        axios
        .get('http://localhost:5002/api/getactiveprof',{
          headers: { Authorization: `${this.token}` },
          })
          .then((response) => {
            if (response.status === 200) {
              this.active_prof = response.data.data;
              console.log('active_prof:', this.active_prof);
            }
          })
          .catch((error) => {
            console.log(error);
          });
      },
      fetchService() {
        axios
          .get('http://localhost:5002/api/service', {
            headers: { Authorization: `${this.token}` },
          })
          .then((response) => {
            if (response.status === 200) {
              this.service = response.data.data;
              
              console.log('service:', this.service);
            }
          })
          .catch((error) => {
            console.log(error);
          });
      },
      
       fetchServiceRequests(){
        axios
          .get(`http://localhost:5002/api/servicerequest/${this.customer_id}`, {
            headers: { Authorization: `${this.token}` },
          })
          .then((response) => {
            if (response.status === 200) {
              this.service_request = response.data.data;
              
              console.log('service:', this.service);
            }
          })
          .catch((error) => {
            console.log(error);
          });

       },

       fetchCompletedRequests(){
        axios
          .get('http://localhost:5002/api/completedservicerequest', {
            headers: { Authorization: `${this.token}` },
          })
          .then((response) => {
            if (response.status === 200) {
              this.completed_service_request = response.data.data;
            }
          })
          .catch((error) => {
            console.log(error);
          });

       }
    },
    mounted() {
    this.active_prof = this.active_prof.map(prof => ({
      ...prof,
      message: "",
      date_of_completion: "",
    }));
  },
}
</script>

<style scoped>
/* Scoped styles for this component */
.dashboard {
  text-align: center;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  height : 770px;
  background-image: url('@/assets/customer.jpg');
  background-position: center; 
  background-size: contain;
}

h1 {
  color: #333;
  font-size: 2em;
}

addservicerequest {
  margin-top: 20px;
  display: inline-block;
  padding: 15px;
  background-color: #007BFF;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

addservicerequest:hover {
  background-color: #0056b3;
}

/* Table styling */
.service-table {
    width: 100%;
    margin: 20px 0;
    border-collapse: collapse;
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .service-table th,
  .service-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }
  
  .service-table th {
    background-color: #b0cf19;
    color: white;
    font-weight: bold;
  }
  
  .service-table td {
    background-color: #f9f9f9;
  }
  
  .service-table tr:hover td {
    background-color: #f1f1f1;
  }
  
  .service-table td button,
  .service-table td a {
    padding: 6px 12px;
    text-decoration: none;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 8px;
  }
  
  .service-table td button {
    background-color: #e74c3c;
    color: white;
    border: none;
  }
  
  .service-table td button:hover {
    background-color: #c0392b;
  }
  
  .service-table td a {
    background-color: #2ecc71;
    color: white;
    text-align: center;
  }
  
  .service-table td a:hover {
    background-color: #27ae60;
  }

  #close{
    background-color:red;
  }
</style>