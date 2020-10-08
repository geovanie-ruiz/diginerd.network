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

  // Enforce plaintext paste
  $('#summernote').on('summernote.paste', function (e, ne) {
    var bufferText = ((ne.originalEvent || ne).clipboardData || window.clipboardData).getData('Text');
    ne.preventDefault();
    bufferText = bufferText.replace(/\r?\n/g, '<br>');
    document.execCommand('insertText', false, bufferText);
  });

  // Lazy loading comments
  $('#loadComments').on('click', function () {
    var link = $(this);
    var page = link.data('page');
    var article = link.data('article');
    $.ajax({
      type: 'post',
      url: '/comments/',
      data: {
        'page': page,
        'article': article,
        'csrfmiddlewaretoken': window.CSRF_TOKEN
      },
      success: function (data) {
        if (data.has_next) {
          link.data('page', page + 1);
        } else {
          link.hide();
        }
        $('#comments').append(data.comments_html);
      },
      error: function (xhr, status, error) { }
    });
  });
})(jQuery); // End of use strict
