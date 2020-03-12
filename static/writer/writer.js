function create(){
var input=document.getElementById("newdocinput");
open("/writer/"+input.value);
}
var timeoutId;
var currentDoc;
$(document).ready(function () {
  currentDoc = document.getElementById("documentIdentifier").innerHTML;
  if (screen.width <= 800) {
    document.getElementById("autoSave").checked = false;
    document.getElementById("saveBtn").style.display = 'block';
  } else {
    document.getElementById("autoSave").checked = true;
    document.getElementById("saveBtn").style.display = "none";
  }
  $('#summernote').summernote({
    fontNames: ['Arial', 'Arial Black', 'Comic Sans MS', 'Courier New', 'Baskerville', 'Gupter', 'Roboto Mono', 'Roboto Condensed', 'Source Sans Pro', 'Merriweather', 'Roboto Slab', 'Calistoga', 'Playfair Display'],
    fontNamesIgnoreCheck: ['Baskerville', 'Gupter', 'Roboto Mono', 'Roboto Condensed', 'Source Sans Pro', 'Merriweather', 'Roboto Slab', 'Calistoga', 'Playfair Display'],
    toolbar: [
      //['paragraph style', ['style', 'ol', 'ul', 'paragraph', 'height']],
      //['font style', ['fontname', 'fontsize', 'color', 'bold', 'underline', 'strikethrough', 'superscript', 'subscript', 'clear']],
      //['insert', ['picture', 'link', 'video', 'table', 'hr']],
      //['misc', ['fullscreen', 'codeview', 'help']]
      ['paragraph', ['style', 'fontname', 'fontsize']],
      ['biuc', ['bold', 'italic', 'underline', 'clear']],
      ['text', ['strikethrough', 'superscript', 'subscript', 'color']],
      ['lists', ['ol', 'ul']],
      ['paragraph2', ['paragraph', 'height']],
      ['insert', ['picture', 'link', 'video', 'table', 'hr']],
      ['misc', ['fullscreen', 'codeview', 'help']]
    ],
    lorem: {
      el: '#summernote', // Element ID or Class used to Initialise Summernote.
      html: true // Place Lorem Ipsum Paragraphs inside <p> or set to false to not too.
    }
  });
  $.ajax({
    url: '/writer/document/' + currentDoc,
    type: 'GET',
    success: function (res) {
      $('#summernote').summernote('code', res);
    }

  })
});
function updateOnlineStatus(event) {
  if (navigator.onLine) {
    document.getElementById("onlineAlert").style.display = "block";
  } else {
    document.getElementById("offlineAlert").style.display = "block";
  }
}
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);
function autoSaveToggle() {
  if (document.getElementById("autoSave").checked) {
    document.getElementById("saveBtn").style.display = "none";
  } else {
    document.getElementById("saveBtn").style.display = 'block';
  }
}
$('#summernote').on('summernote.change', function (we, contents, $editable) {
  //Thanks https://chevtek.io/how-to-implement-autosave-in-your-web-app/
  if (timeoutId) clearTimeout(timeoutId);
  timeoutId = setTimeout(function () {
    we.preventDefault();
    var id_value = contents;
    // Do an AJAX post
    if (document.getElementById("autoSave").checked) {
      $.ajax({
        type: "POST",
        url: "/writer/save/" + currentDoc,
        data: {
          editordata: id_value // various ways to store the ID, you can choose
        },
        success: function (data) {
          // POST was successful - do something with the response

        },
        error: function (data) {
          // Server error, e.g. 404, 500, error
        }
      });
    }
  }, 750)
});

$('div.note-emojionechar-dialog').attr('tabindex', '-1');