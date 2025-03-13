$(document).ready(function () {
  $(".owll-carousel").owlCarousel({
      loop: true,
      margin: 10,
      nav: true,
      dots: false,
      autoplay: true, 
      autoplayTimeout: 2000, 
      autoplayHoverPause: true, 
      responsive: {
          0: {
              items: 1,
          },
          576: {
              items: 2, 
          },
          768: {
              items: 3, 
          },
          1024: {
              items: 4,
          },
      },
  });
});
