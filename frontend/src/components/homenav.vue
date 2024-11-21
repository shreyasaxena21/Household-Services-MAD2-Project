<template>
    <nav class="navbar">
      <div class="navbar-links">
        <h4 style="font-family: Georgia, 'Times New Roman', Times, serif;">A-Z Household Services</h4>
        <router-link to="/" class="nav-link" active-class="active">Home</router-link> |
        <router-link to="/login" class="nav-link" active-class="active">Login</router-link> |
        <router-link to="/Register" class="nav-link" active-class="active">Register</router-link> |
        <router-link to="/about" class="nav-link" active-class="active">About</router-link> 
       
      </div>
    </nav>
    <router-view />
  </template>
  
  <script>
  export default {
    name: 'homenav',
  };
  </script>
  
  <style scoped>
  /* Base styles for the navigation bar */
  .navbar {
    background-color: #3091bb; /* Blue background */
    padding: 10px 10px;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 1rem;
    border-radius: 10px;
  }
  
  .navbar-links {
    display: flex;
    justify-content: space-around;
    align-items: center;
  }
  
  .nav-link {
    color: white;
    text-decoration: none;
    padding: 8px 12px;
    border-radius: 4px;
    font-weight: 500;
    transition: background-color 0.3s ease, color 0.3s ease;
    align-content: center;
    font-family: Georgia, 'Times New Roman', Times, serif;
  }
  
  .nav-link:hover {
    background-color: #13467c; /* Darker blue for hover effect */
    color: #fff; /* Keep text white on hover */
  }
  
  
  
  .nav-link.logout {
    background-color: #e74c3c; /* Red for logout button */
    color: white;
  }
  
 
  /* Responsive design for smaller screens */
  @media (max-width: 768px) {
    .navbar {
      flex-direction: column;
      text-align: center;
    }
  
    .navbar-links {
      flex-direction: column;
      width: 100%;
    }
  
    .nav-link {
      margin: 5px 0;
    }
  }
  </style>
  