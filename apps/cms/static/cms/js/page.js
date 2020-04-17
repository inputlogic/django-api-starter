(function ($) {
  $(function () {
    const $layoutSelect = $('#id_layout')
    const $layoutSimple = $('fieldset.layout_simple')
    const $layoutSectioned = $('.layout_sectioned')

    const toggleSections = (val) => {
      if (val === 'simple') {
        $layoutSimple.show()
        $layoutSectioned.hide()
      } else if (val === 'sectioned') {
        $layoutSimple.hide()
        $layoutSectioned.show()
      }
    }

    toggleSections($layoutSelect.val())
    $layoutSelect.change(() => {
      toggleSections($layoutSelect.val())
    })
  })
}(window.django.jQuery));
