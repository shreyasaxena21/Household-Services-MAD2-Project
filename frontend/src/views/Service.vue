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
              <router-link :to="{ name: 'updateService', params: { id: serv.id } }" id="update">Update</router-link> | 
              <button v-if="!serv.delete" type="button" @click="deleteservice(serv.id)" id="delete">Delete</button>
            </td>
          </tr>
        </tbody>
      </table><br>
      <router-link to="/addService" id="addservice">Add New Service</router-link>
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
  height: 700px;
  background-color:rgb(166, 239, 247);
  background-image: url('@/assets/admin.jpg');
  background-position: center; 
  background-size: contain;
 
  
}
  
.service-table {
  width: 100%;
  border-collapse: collapse;
  margin: 0 auto;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.service-table th,
.service-table td {
  padding: 10px;
  text-align: left;
  border: 1px solid #ddd;
}

.service-table th {
  background-color: #3479ab;
  color: white;
  font-family: Georgia, "Times New Roman", Times, serif;
}

.service-table tr:nth-child(even) {
  background-color: #f6fcfd;
}

.service-table tr:hover {
  background-color: #fafbf7;
}

  
#update {
  display: inline-block;
  padding: 10px 20px;
  background-color: rgb(82, 196, 82);
  color: white;
  text-align: center;
  text-decoration: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

#update:hover {
  background-color: green;
}

#delete {
  display: inline-block;
  padding: 10px 20px;
  background-color: rgb(224, 25, 25);
  color: white;
  text-align: center;
  text-decoration: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

#delete:hover {
  background-color: rgb(126, 31, 14);
}
  
#addservice {
  display: inline-block;
  padding: 10px 20px;
  background-color: rgb(3, 120, 3);
  color: white;
  text-align: center;
  text-decoration: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

#addservice:hover {
  background-color: rgb(2, 66, 2);
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
  