<template>
    <div class="dashboard">
        <custnav></custnav>

        <form class="search" @submit.prevent="search">
            <input type="text" v-model="this.search_word" class="input" placeholder="Search by location, service type"/><button class="search-button" @click="search()">Search</button>
        </form><br><br>
        <h2 v-if="search_word">Search Results for "{{ search_word }}"</h2>
      <ul v-if="results && results.length">
        <li v-for="result in results" :key="result.professional_id">
          <strong>Service:</strong> {{ result.service_name }}<br />
          <strong>Professional:</strong> {{ result.professional_name }}<br />
          <strong>Email:</strong> {{ result.professional_email }}<br />
          <strong>Experience:</strong> {{ result.professional_experience }} years<br />
          <hr />
        </li>
      </ul>
      <!-- <p v-else>No results found.</p> -->
      

        <h3 style="font-family: Georgia, 'Times New Roman', Times, serif;">Service Professionals</h3>
      <table class="service-table">
        <thead>
          <tr>
            <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Id</th>
            <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Name</th>
            <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Email</th>
            <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Service Type</th>
            <th style="font-family: Georgia, 'Times New Roman', Times, serif;">Experience</th>

          </tr>
        </thead>
        <tbody>
          <tr v-for="active in active_prof" :key="active.id">
            <td>{{ active.id }}</td>
            <td>{{ active.name }}</td>
            <td>{{ active.email }}</td>
            <td>{{ active.service_type }}</td>
            <td>{{ active.experience }} Years</td>

          </tr>
        </tbody>
      </table>

      

    </div>
  </template>
  
  <script>
import axios from 'axios';
import custnav from '../components/custnav.vue'
  
export default {
    name: "customersearch",
    components : {
        custnav

    },

    data() {
      return {
        search_word: null, 
        results: [], 
        token: null,
        active_prof:[],
        active_prof_id : null
      };
    },

    created() {
        this.token = localStorage.getItem('authtoken');
        if (!this.token) { 
          this.$router.push('/login');
        } else{
            
            this.fetchActiveProfessional()
        }
    },

    methods: {
        search(){
            if (!this.search_word) {
          alert("Please enter a search term.");
          }


            axios
          .get(`http://localhost:5002/api/adminsearch/${this.search_word}`, {
          },{
            headers: { Authorization: `Bearer ${this.token}` },
          })
          .then((response) => {
            if (response.status === 200) {
              this.results = response.data.data;
              console.log('result:', this.result);
            }
          })
          .catch((error) => {
            console.log(error);
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
      }
      
    }
  }
    
  
  </script>
  
  <style scoped>
 .dashboard {
      text-align: center;
      font-family: Arial, sans-serif;
      height: 100%;
      padding: 20px;
      border-radius: 5px;
      height: 750px;
      background-color:rgb(166, 239, 247);
      background-image: url('@/assets/customer.jpg');
      background-position: center; 
      background-size: contain;

      
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
  

  .search{
  display: flex;
  justify-content: center;
  margin: auto;
  margin-top: 30px;
  
}

.input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px 0 0 5px;
  width: 300px;
}

.search-button {
  background-color: #fcae27;
  color: white;
  border: none;
  border-radius: 0 5px 5px 0;
  padding: 10px 20px;
  cursor: pointer;
}

.search-button:hover {
  background-color: #a48d26;
}

  h2 {
    text-align: center;
    margin-top: 20px;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    margin-bottom: 20px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  
  hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 10px 0;
  }
  
  p {
    text-align: center;
    margin-top: 20px;
    color: #555;
  }

  #flag {
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
}

#flag:hover {
  background-color: #b02a37;
}
  </style>
  