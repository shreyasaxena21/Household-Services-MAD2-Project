<template>
    <div class="dashboard">
      <pronav></pronav>
      <div class="graphs-container">
        <h2 class="graphs-heading" style="font-family: Georgia, 'Times New Roman', Times, serif;">Statistics</h2>
        <div class="graphs-row">

          
          <!-- Display dynamic histogram image -->
          <img
            v-if="histogramImage"
            :src="histogramImage"
            alt="Service Request Bar Graph"
            class="graph-image"
          />
          <p v-else>Loading Statistics...</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import pronav from "../components/pronav.vue";
  
  export default {
    name: "profstats",
    components: {
      pronav,
    },
    data() {
      return {
        token: null,
        id : localStorage.getItem('id'),
        histogramImage : "", 
   
  
      };
    },
  
    created() {
      this.token = localStorage.getItem("authtoken");
      if (!this.token) {
        this.$router.push("/login"); // Redirect to login if no token
      } else {
        this.fetchStatistics(); // Fetch stats data
      }
    },
  
    methods: {
      fetchStatistics() {
        // Fetch the pie chart
        axios
          .get(`http://localhost:5002/api/showprofstats/${this.id}`, {
            headers: { Authorization: `${this.token}` },
          })
          .then((response) => {
            if (response.status === 200) {
              console.log("Pro Stats:", response.data);
              
              this.histogramImage = `data:image/png;base64,${response.data.histogram}`; // Dynamically load bar graph
         
            }
          })
          .catch((error) => {
            console.error("Error fetching pie chart:", error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
   .dashboard {
        text-align: center;
        font-family: Arial, sans-serif;
        height: 100%;
        padding: 20px;
        border-radius: 5px;
        height: 1050px;
        background-color:rgb(166, 239, 247);
        background-image: url('@/assets/professional.jpg');
        background-position: center; 
      
        
        
  }
  
  .graphs-container {
    margin-top: 50px;
    text-align: center;
  }
  
  .graphs-heading {
    font-size: 24px;
    color: #2c3e50;
    margin-bottom: 20px;
  }
  
  .graphs-row {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-bottom: 30px;
  }
  
  .graph-image {
    max-width: 45%;
    height: auto;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
  </style>
  
  
  
  
  
   