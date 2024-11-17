  
  function menuBar() {
      menuList = document.getElementById("menu-list");
      
      menuList.classList.toggle('open')
      
      mainContent = document.getElementById("main-content");
      mainContent.classList.toggle('main-content-border-control')
  }
  