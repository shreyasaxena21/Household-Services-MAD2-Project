<template>
  <div class="dashboard">
  <homenav></homenav>
  <div id="home">
      <div id="welcome">
        <h1>Welcome to A-Z Household Services App!</h1>
        <h2>
          <h3>
           Introducing A-Z Household Services, your ultimate solution for all home maintenance and servicing needs!  A multi-user app that acts as a platform for providing comprehensive home servicing and solutions. This multi-user app connects homeowners with trusted and skilled professionals, providing a seamless platform for efficient and reliable home services.
           Whether you're looking for a plumber, electrician, cleaner, or handyman, A-Z Household Services has you covered. Our app simplifies the process of finding and booking top-rated service providers in your area, ensuring your home is always in perfect shape.
          </h3> <br>

          <h3>At A-Z Household Services, we understand that your home requires various types of maintenance, and we offer a wide range of services to cater to every need. Whether you're looking to fix a leaky faucet, repair an electrical issue, or clean your carpets, we have an expert for every job. Our categories include:
            <ul>
              
              <li>Plumbing: Fix leaks, install new plumbing systems, unclog drains, and much more.</li>
              <li>Electrical: Wiring, lighting, repairs, and electrical troubleshooting.</li>
              <li>Cleaning: Deep cleaning, carpet cleaning, window washing, and regular housekeeping.</li>
              
            </ul>
          </h3>


        </h2>
      </div>
    </div>
  </div>
</template>

<script>

import homenav from '../components/homenav.vue'
export default {
  name: 'HomeView',
  components :{
    homenav
  }
}
</script>


<style scoped>

.dashboard{
  background-image: url('@/assets/home.webp');
  background-size: cover; 
  background-repeat: no-repeat; 
  background-position: center; 
  height: 750px;

}

#home {
  
  display: flex; 
  align-items: flex-start; 
  justify-content: center;

  /* color: black; */
  padding: 20px;
  margin: 0;
}

#welcome {
  margin-top: 50px;
  text-align: center; /* Center-align text */
  background: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
  padding: 30px;
  border-radius: 15px; 
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.3); 
  max-width: 80%; 
}

h1{
  color: rgb(12, 126, 128);
  background-color: rgb(195, 216, 121);
  border-radius: 10px;
  font-family: 'Times New Roman', Times, serif;

}

h2 h3 {
  color: rgb(60, 60, 60);
  font-size: 1.2rem;
  line-height: 1.5;
  margin: 0;
  font-weight: 400; /* Subtle font weight for readability */
}
</style>