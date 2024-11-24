<template>
  <homenav></homenav>
    <div id="home">
      <h1 style="color:black; font-family: Georgia, 'Times New Roman', Times, serif; ">Welcome to Household Services App!!!</h1>
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
#home {
  background-image: url('https://www.housecallpro.com/wp-content/uploads/2024/04/home-service-business-ideas.webp');
  background-size: cover; 
  background-repeat: no-repeat; 
  background-position: center; 
  height: 100vh; 
  display: flex; 
  align-items: flex-start; 
  justify-content: center;
  /* color: black; */
  padding: 20px;
  margin: 0;
}
</style>