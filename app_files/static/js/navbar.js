// JS from startbootstrap.com

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#navbarMain").offset().top > 50) {
      $("#navbarMain").addClass("navbar-shrink");
    } else {
      $("#navbarMain").removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);