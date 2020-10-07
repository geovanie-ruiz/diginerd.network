(function ($) {
  "use strict";

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function () {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 80
  });

  // Collapse Navbar
  var navbarCollapse = function () {
    var mainNav = $('#mainNav');
    if (mainNav.length) {
      if ($("#mainNav").offset().top > 100) {
        $("#mainNav").addClass("navbar-shrink");
      } else {
        $("#mainNav").removeClass("navbar-shrink");
      }
    }
  };

  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  $(document).ready(function () {
    $(".close").click(function () {
      $("#myAlert").alert("close");
    });
  });

  // Summernote input form
  $(document).ready(function () {
    $('#summernote').summernote({
      toolbar: [
        ['misc', ['undo', 'redo']],
        ['style', ['bold', 'italic', 'underline', 'clear']],
        ['list', ['ul', 'ol']],
      ],
      placeholder: 'What are your thoughts?',
      tabsize: 2,
      height: 300,
      disableDragAndDrop: true
    });
  });

  // Lazy loading comments
  $('#loadComments').on('click', function () {
    var link = $(this);
    var page = link.data('page');
    $.ajax({
      type: 'post',
      url: '/comments/',
      data: {
        'page': page,
        'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
      },
      success: function (data) {
        // if there are still more pages to load,
        // add 1 to the "Load More Posts" link's page data attribute
        // else hide the link
        if (data.has_next) {
          link.data('page', page + 1);
        } else {
          link.hide();
        }
        // append html to the posts div
        $('#comments').append(data.comments_html);
      },
      error: function (xhr, status, error) {
        // shit happens friends!
      }
    });
  });
})(jQuery); // End of use strict
