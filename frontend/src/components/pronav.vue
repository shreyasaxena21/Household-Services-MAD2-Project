<template>
    <nav class="navbar">
      <div class="navbar-links">
        <h4 style="font-family: Georgia, 'Times New Roman', Times, serif;">Professional Dashboard</h4>
        <router-link to="/professionaldashboard" class="nav-link" active-class="active">Home</router-link> |
        <router-link to="/" class="nav-link" active-class="active">Search</router-link> |
        <router-link to="/" class="nav-link" active-class="active">Summary</router-link> |
        <router-link to="/editprofessionalprofile" class="nav-link" active-class="active">Edit Profile</router-link> |
        <a @click="logout" class="nav-link logout">Logout</a>     
      </div>
    </nav>
    <router-view />
  </template>
  
  <script>
  export default {
    name: 'pronav',
    methods: {
      logout() {
        localStorage.clear();
        this.$router.push('/login'); // Redirect to login after logging out
      },
    },
  };
  </script>
  
  <style scoped>
  /* Base styles for the navigation bar */
  .navbar {
    background-color:   #861996; /* Blue background */
    padding: 10px 20px;
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
    background-color: #0056b3; /* Darker blue for hover effect */
    color: #fff; /* Keep text white on hover */
  }
  
  .nav-link.active {
    background-color: #f39c12; /* Yellow for the active link */
    color: white;
  }
  
 
  
  .nav-link.logout:hover {
    background-color: #c0392b; /* Darker red on hover */
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
  