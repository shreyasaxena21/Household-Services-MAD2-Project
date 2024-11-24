<template>
    
    <div id="dashboard">
      <adminnav></adminnav> 
        <div class="graphs-container">
            <h2 class="graphs-heading">Statistics</h2>
            <div class="graphs-row">
             <img src="" alt="Services Pie Chart" class="graph-image"/>
            <!-- <img src="../assets/behaviour.png" alt="User Request Behavior" class="graph-image"/> -->
            </div>
            <!-- <div class="graphs-row">
            <img src="../assets/histo.png" alt="Requests Histogram" class="graph-image"/>
            <img src="../assets/bar.png" alt="Interesting Plot" class="graph-image"/>
            </div> -->
        </div>
    </div>
  </template>
  
  
  <script>
  import axios from 'axios';
  import adminnav from '../components/adminnav.vue';
  
  export default {
    name: 'adminstats',
    components: {
      adminnav,
    },

    data(){
        return {
            token : null
        }
  
    },

    created(){
        this.token = localStorage.getItem('authtoken');
      if (!this.token) {
        this.$router.push('/login');
      } else {
        this.adminstats();
      }

    },

    methods: {
        adminstats(){
            axios
            .get('http://localhost:5002/api/showadminsstats',{
            headers: { Authorization: `${this.token}` },
          })
          .then((response) => {
            if (response.status === 200) {
              console.log("Admin Stats");
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
  