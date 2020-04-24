// Enables collapsable sections in Django admin, that default to open.
// Usage: when using class `collapse` in django admin, also include class `show`
(function (_, doc) {
  doc.addEventListener("DOMContentLoaded", function () {
    _.setTimeout(function () {
      var $ = _.django.jQuery
      var fieldsetsToShow = doc.querySelectorAll('.collapsed.show');
      for (var x = 0; x < fieldsetsToShow.length; x++) {
        var fieldset = fieldsetsToShow[x];
        var $toggle = $(fieldset.querySelector('.collapse-toggle'));
        $toggle.text(gettext('Hide'));
        fieldset.classList.remove('collapsed');
      };
    }, 100);
  });
}(window, document));
