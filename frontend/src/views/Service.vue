<template>
    <div class = "dashboard">
      <adminnav></adminnav>
      <h3 style="font-family: Georgia, 'Times New Roman', Times, serif;"> Services</h3>
      <table class="service-table">
        <thead>
          <tr>
            <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Id</th>
            <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Name</th>
            <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Description</th>
            <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Time Required</th>
            <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Base Price</th>
            <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="serv in service" :key="serv.id">
            <td>{{ serv.id }}</td>
            <td>{{ serv.name }}</td>
            <td>{{ serv.description }}</td>
            <td>{{ serv.time_required }} Hours</td>
            <td>{{ serv.price }}</td>
            <td>
              <router-link :to="{ name: 'updateService', params: { id: serv.id } }" class="btn btn-update">Update</router-link> 
              <button v-if="!serv.delete" type="button" @click="deleteservice(serv.id)" class="btn btn-delete">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <router-link to="/addService" class="nav-link btn-style">Add New Service</router-link>
      <!-- <button type="button" id="addservice"> Add New Service</button> -->
    </div>
  </template>
  
  <script>
  import adminnav from '../components/adminnav.vue';
  import addService from '../views/AddService.vue';
  import axios from 'axios';
  export default{
    components: { adminnav },
    name: 'service',
    data() {
      return {
        token: null,
        message: null,
        service: [],
        service_id: null,
      };
    },
    created() {
      this.token = localStorage.getItem('authtoken');
      if (!this.token) {
        this.$router.push('/login');
      } else {
        this.fetchService();
      }
    },
    methods: {
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
      deleteservice(id) {
        axios
          .delete(`http://localhost:5002/api/service/${id}`, {
            headers: { Authorization: `${this.token}` },
          })
          .then((response) => {
            if (response.status === 200) {
              console.log(response);
              this.fetchService();
              alert("Service deleted successfully!")
              location.reload();
            }
          })
          .catch((error) => {
            console.log(error);
          });
      },
    }
  }
  </script>
  
  <style scoped>
  /* General styles for the service table */
  .dashboard {
  text-align: center;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
}
  
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
    background-color: #007bff;
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
  
  .btn-style {
  display: inline-block;
  padding: 10px 20px;
  background-color: rgb(33, 121, 33);
  color: white;
  text-align: center;
  text-decoration: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-style:hover {
  background-color: green;
}
  
  /* Responsive table */
  @media (max-width: 768px) {
    .service-table {
      font-size: 14px;
    }
  
    .service-table th,
    .service-table td {
      padding: 10px;
    }
  
    .dashboard-container {
      padding: 20px;
    }
  
    h1 {
      font-size: 2rem;
    }
  }
  </style>
  