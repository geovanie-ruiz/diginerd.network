(function ($) {
  "use strict";

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

  // Lazy loading content
  $('#loadContent').on('click', function () {
    var link = $(this);
    var page = link.data('page');
    var container = link.data('container');
    var term = link.data('term');
    var filtered = Boolean(link.data('filtered'));
    var content;

    switch (link.data('type')) {
      case 0:
        content = 'articles';
        break;
      case 1:
        content = 'comments';
        break;
      case 2:
        content = 'cards';
        break;
    }

    $.ajax({
      type: 'post',
      url: ''.concat('/load-', content, '/'),
      data: {
        'page': page,
        'container': container,
        'csrfmiddlewaretoken': window.CSRF_TOKEN,
        'term': term,
        'filtered': filtered
      },
      success: function (data) {
        if (data.has_next) {
          link.data('page', page + 1);
        } else {
          link.hide();
        }
        $(''.concat('#', content)).append(data.contents_html);
      },
      error: function (xhr, status, error) { }
    });
  });

  // Discreet search validation
  document.addEventListener('invalid', (function () {
    return function (e) {
      e.preventDefault();
      document.getElementById("cardSearch").focus();
    };
  })(), true);

})(jQuery); // End of use strict
