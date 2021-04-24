// Change navbar background color on scroll
var setNavbarColor = function() {
  if ($("#navbarMain").offset().top > 50) {
    $("#navbarMain").addClass("c-bg-dark");
  } else {
    $("#navbarMain").removeClass("c-bg-dark");
  }
};
setNavbarColor();
$(window).scroll(setNavbarColor);
