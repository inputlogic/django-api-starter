window.QUILLS = window.QUILLS || {};

if (!QUILLS[id]) {
  console.log('init Quill', { id, $e });
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
}
