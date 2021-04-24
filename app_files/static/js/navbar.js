// Change navbar background color on scroll
var setNavbarColor = function() {
  if ($("#navbarMain").offset().top > 50) {
    $("#navbarMain").addClass("bg-dark");
  } else {
    $("#navbarMain").removeClass("bg-dark");
  }
};
setNavbarColor();
$(window).scroll(setNavbarColor);
