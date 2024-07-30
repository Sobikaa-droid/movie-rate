window.addEventListener('scroll', function() {
    localStorage.setItem('scrollPosition', window.pageYOffset);
  });

  window.addEventListener('load', function() {
    var scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition) {
      window.scrollTo(0, scrollPosition);
    }
  });