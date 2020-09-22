(function (window) {
  window.QUILLS = window.QUILLS || {};

  if (!QUILLS[id]) {
    console.log('init Quill', { id, $e, settings });
    // Hide the textarea element
    $e.hide();

    // Create a div to use for our quill editor, initialized with
    // the contents of the django rendered textarea.
    var $quill = $('<div id="' + id + '_quill">' + $e.val() + '</div>');
    $quill.insertAfter($e);

    // Initialize Quill on the new div, and sync changes back to the textarea.
    QUILLS[id] = new Quill('#' + id + '_quill', settings);
    QUILLS[id].on('text-change', function (delta, oldDelta, source) {
      $e.val(QUILLS[id].container.firstChild.innerHTML)
    });

    // Add image upload handler.
    var toolbar = QUILLS[id].getModule('toolbar');
    toolbar.addHandler('image', imageHandler); 
  }

  function imageHandler (editor, path) {
    var input = document.createElement('input');

    input.setAttribute('type', 'file');
    input.setAttribute('accept', 'image/*');
    input.click();

    input.onchange = function () {
      console.log('handle image', path, input.files[0]);
      uploadImage(input.files[0])
        .then(function (resp) {
          const range = QUILLS[id].getSelection(true);
          console.log('uploadImage', resp);
          QUILLS[id].insertEmbed(range.index, 'image', resp.url);
        });
    }
  }

  function uploadImage (file) {
    return new Promise(function (resolve, reject) {
      var resp;
      getSignedFile(file)
        .then(function (res) {
          resp = res;
          console.log('uploadFile', resp);
          return uploadFile(file, resp.s3Data);
        })
        .then(function () {
          resolve(resp);
        })
        .catch(function (err) {
          console.error(err);
          reject(err);
        });
    });
  }

  function getSignedFile (file) {
    const data = {
      acl: 'public-read',
      fileName: file.name,
      contentType: file.type
    };
    return new Promise(function (resolve, reject) {
      window.fetch('/files', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest",
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          return res.json();
        })
        .then(function (data) {
          resolve(data);
        })
        .catch(function (err) {
          console.error('getSignedFile', err);
        });
    }); 
  }

  function uploadFile (file, s3Data) {
    var formData = new window.FormData();
    for (var key in s3Data.fields) {
      formData.append(key, s3Data.fields[key]);
    }
    formData.append('file', file);
    return window.fetch(s3Data.url, {method: 'POST', body: formData});
  }

  function getCookie (name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }

    return cookieValue;
  }
})(window);
