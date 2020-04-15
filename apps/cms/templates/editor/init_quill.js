window.QUILLS = window.QUILLS || {};
if (!QUILLS[id]) {
  $e.hide();
  var $quill = $('<div id="' + id + '_quill">' + $e.val() + '</div>');
  $quill.insertAfter($e);
  $quill.css('min-width', 700);
  $quill.css('min-height', 400);
  QUILLS[id] = new Quill('#' + id + '_quill', settings);
  QUILLS[id].on('text-change', function (delta, oldDelta, source) {
    $e.val(QUILLS[id].container.firstChild.innerHTML)
  });
}
