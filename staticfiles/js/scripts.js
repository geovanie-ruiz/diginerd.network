(function ($) {
  "use strict";

  // Summernote minimum length
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

  // Sumernote in-page edit
  $("#comments").on("click", "button", function (event) {
    event.preventDefault();
    var el = $(this);
    var btn = el[0];
    var commentId = el.data('comment');
    var url = el.data('url');
    var slug = el.data('slug');

    if (btn.id.includes('edit')) {
      document.getElementById('edit' + commentId).setAttribute('disabled', 'true');
      document.getElementById('save' + commentId).removeAttribute('disabled');
      $('#comment' + commentId + 'Text').summernote({
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
        hint: {
          match: /\B@(\w*)$/,
          cards: function (keyword, callback) {
            $.ajax({
              type: 'post',
              url: '/card-mention/',
              data: {
                'term': keyword,
                'csrfmiddlewaretoken': window.CSRF_TOKEN
              }
            }).done(callback);
          },
          search: function (keyword, callback) {
            this.cards(keyword, callback);
          },
          template: function (item) {
            return item.name;
          },
          content: function (item) {
            var node = document.createElement('a');
            node.append('@' + item.name);
            node.setAttribute('href', '/cards/card-details/' + item.number);
            node.setAttribute('class', 'card-popover');
            node.setAttribute('data-card', item.number);
            return node;
          }
        },
        tabsize: 2,
        height: 150,
        disableDragAndDrop: true,
        focus: true
      });
      $('#comment' + commentId + 'Text').summernote("removeModule", "linkPopover");
    } else if (btn.id.includes('save')) {
      var markup = $('#comment' + commentId + 'Text').summernote('code');
      $.ajax({
        type: 'post',
        url: '/new-comment/',
        data: {
          'editordata': markup,
          'url': url,
          'slug': slug,
          'commentId': commentId,
          'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success: function (data) {
          $('#comment' + commentId + 'Text').summernote('destroy');
          document.getElementById('edit' + commentId).removeAttribute('disabled');
          document.getElementById('save' + commentId).setAttribute('disabled', 'true');
        },
        error: function (xhr, status, error) { }
      });
    }
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
      hint: {
        match: /\B@(\w*)$/,
        cards: function (keyword, callback) {
          $.ajax({
            type: 'post',
            url: '/card-mention/',
            data: {
              'term': keyword,
              'csrfmiddlewaretoken': window.CSRF_TOKEN
            }
          }).done(callback);
        },
        search: function (keyword, callback) {
          this.cards(keyword, callback);
        },
        template: function (item) {
          return item.name;
        },
        content: function (item) {
          var node = document.createElement('a');
          node.append('@' + item.name);
          node.setAttribute('href', '/cards/card-details/' + item.number);
          node.setAttribute('class', 'card-popover');
          node.setAttribute('data-card', item.number);
          return node;
        }
      },
      tabsize: 2,
      height: 300,
      disableDragAndDrop: true
    });
    $("#summernote").summernote("removeModule", "linkPopover");
  });

  // Lazy loading comments
  $('#loadComments').on('click', function () {
    var link = $(this);
    var page = link.data('page');
    var redirect_url = link.data('url');
    var container = link.data('container');

    $.ajax({
      type: 'post',
      url: '/load-comments/',
      data: {
        'page': page,
        'container': container,
        'redirect_url': redirect_url,
        'csrfmiddlewaretoken': window.CSRF_TOKEN
      },
      success: function (data) {
        if (data.has_next) {
          link.data('page', page + 1);
        } else {
          link.hide();
        }
        $('#comments').append(data.contents_html);
      },
      error: function (xhr, status, error) { }
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

  // Discrete search validation
  document.addEventListener('invalid', (function () {
    return function (e) {
      e.preventDefault();
      document.getElementById(e.target.id).focus();
    };
  })(), true);

})(jQuery); // End of use strict
