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
      callbacks: {
        onKeydown: function (e) {
          var t = e.currentTarget.innerText;
          if (t.trim().length >= 5000) {
            //delete keys, arrow keys, copy, cut, select all
            if (e.keyCode != 8 && !(e.keyCode >= 37 && e.keyCode <= 40) && e.keyCode != 46 && !(e.keyCode == 88 && e.ctrlKey) && !(e.keyCode == 67 && e.ctrlKey) && !(e.keyCode == 65 && e.ctrlKey))
              e.preventDefault();
          }
        },
        onKeyup: function (e) {
          var t = e.currentTarget.innerText;
          var textLen = t.trim().length;
          if (textLen >= 4950) {
            $('.note-status-output').html(
              '<span class="text-danger">' + textLen + ' out of 5000 characters.' + '</span>'
            );
          } else if (textLen >= 4000) {
            $('.note-status-output').html(
              '<span class="text-warning">' + textLen + ' out of 5000 characters.' + '</span>'
            );
          } else if (textLen <= 30) {
            $('.note-status-output').html('');
          }
        },
        onPaste: function (e) {
          var t = e.currentTarget.innerText;
          var bufferText = ((e.originalEvent || e).clipboardData || window.clipboardData).getData('Text');
          bufferText = bufferText.replace(/\r?\n/g, '<br>');
          e.preventDefault();
          var maxPaste = bufferText.length;
          if (t.trim().length + maxPaste > 5000) {
            maxPaste = 5000 - t.trim().length;
          }
          document.execCommand('insertText', false, bufferText.substring(0, maxPaste));
          if ((t.trim().length + maxPaste) >= 4000) {
            $('.note-status-output').html((t.trim().length + maxPaste) + ' out of 5000 characters');
          }
        }
      },
      tabsize: 2,
      height: 300,
      disableDragAndDrop: true
    });
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
      document.getElementById(e.target.id).focus();
    };
  })(), true);

  document.addEventListener('submit', (function () {
    return function (e) {
      if (e.submitter.id == 'submitComment') {
        var cLen = $('.note-editable').text().length;
        if (cLen < 30) {
          e.preventDefault();
          $('.note-status-output').html(
            '<span class="text-danger">' + cLen + ' out of 30 character minimum.' + '</span>'
          );
        }
      };
    };
  })(), true);

})(jQuery); // End of use strict
