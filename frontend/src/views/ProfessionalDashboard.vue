<template>
    <div class="dashboard">
      <pronav></pronav>
      <h3>Welcome {{ this.name }}</h3>

      <h3 style="font-family: Georgia, 'Times New Roman', Times, serif;">Customer Requests</h3>
          <table class="service-table">
            <thead>
              <tr>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Id </th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Customer Name </th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Location </th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Pincode </th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Message </th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Date of Completion</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Actions</th>

              </tr>
            </thead>
            <tbody>
              <tr v-for="request in customer_request" :key="request.id">
                <td>{{ request.id }}</td>
                <td>{{ request.cust_name }}</td>
                <td>{{ request.cust_city }}</td>
                <td>{{ request.pincode }}</td>
                <td>{{ request.message }}</td>
                <td>{{ request.date_of_completion }}</td>
                <td>
                  <button type="button" @click="accept(request.id)" style="background-color: green;">Accept</button>
                  <button type="button" @click="reject(request.id)" style="background-color: red;">Reject</button>
               </td>
              </tr>
            </tbody>
          </table>

          <h3 style="font-family: Georgia, 'Times New Roman', Times, serif;">Accepted/Completed Requests</h3>
          <table class="service-table">
            <thead>
              <tr>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Id </th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Customer Name </th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Location </th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Pincode </th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Message </th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Date of Completion</th>
                <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Status</th>

              </tr>
            </thead>
            <tbody>
              <tr v-for="request in accepted_request" :key="request.id">
                <td>{{ request.id }}</td>
                <td>{{ request.cust_name }}</td>
                <td>{{ request.cust_city }}</td>
                <td>{{ request.pincode }}</td>
                <td>{{ request.message }}</td>
                <td>{{ request.date_of_completion }}</td>
                <td>{{ request.service_status }}</td>
               
              </tr>
            </tbody>
          </table>

    </div>
  </template>
  
<script>
import axios from 'axios'
import pronav from '../components/pronav.vue'
export default{
  
    name : "professionaldashboard",
    components : {
      pronav
    },
    data() {
      return {
        id : localStorage.getItem('id'),
        token: null,
        customer_request : [],
        customer_request_id : null,
        service_status : null,
        accepted_request:[],
        name : localStorage.getItem('name')
        
      };
    },

    created() {
      this.token = localStorage.getItem('authtoken');
      if (!this.token) {
        this.$router.push('/login');
      } else {
        this.fetchCustomerRequests();
        this.fetchAcceptedRequests();
       
      }
    },
    methods: {
      
       fetchCustomerRequests(){
        axios
          .get(`http://localhost:5002/api/customerrequest/${this.id}`, {
            headers: { Authorization: `${this.token}` },
          })
          .then((response) => {
            if (response.status === 200) {
              this.customer_request = response.data.data;
              
              
            }
          })
          .catch((error) => {
            console.log(error);
          });

       },

       accept(id){
        axios
        .put(`http://localhost:5002/api/acceptrequest/${id}`,{
             service_status : "Assigned"
        } ,{

          headers: { Authorization: `${this.token}` },
          })
          .then((response) => {
            if (response.status === 200) {
              alert("Request Accepted!")
              location.reload()
              
              
            }
          })
          .catch((error) => {
            console.log(error);
          });
        },

        reject(id){
          axios
        .put(`http://localhost:5002/api/rejectrequest/${id}`,{
          service_status : "Rejected"
        } ,{

          headers: { Authorization: `${this.token}` },
          })
          .then((response) => {
            if (response.status === 200) {
              alert("Request Rejected!")
              location.reload()
              
              
            }
          })
          .catch((error) => {
            console.log(error);
          });
        

       },

       fetchAcceptedRequests(){
        axios
          .get(`http://localhost:5002/api/acceptedrequests/${this.id}`, {
            headers: { Authorization: `${this.token}` },
          })
          .then((response) => {
            if (response.status === 200) {
              this.accepted_request = response.data.data;
              
              
            }
          })
          .catch((error) => {
            console.log(error);
          });

       }

  },

       

      //  fetchCompletedRequests(){
      //   axios
      //     .get('http://localhost:5002/api/completedservicerequest', {
      //       headers: { Authorization: `${this.token}` },
      //     })
      //     .then((response) => {
      //       if (response.status === 200) {
      //         this.completed_service_request = response.data.data;
      //       }
      //     })
      //     .catch((error) => {
      //       console.log(error);
      //     });

      //  }
    // },
    // mounted() {
    // this.active_prof = this.active_prof.map(prof => ({
    //   ...prof,
    //   message: "",
    //   date_of_completion: "",
    // }));
  
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
  height : 730px;
  background-image: url('@/assets/professional.jpg');
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
    background-color: #861996;
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
