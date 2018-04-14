// Verify that only one layout instance is currently marked as active. This
// should really be done on the backend--ideally at the database level--but
// Django admin makes this too hard, so this should suffice for now.
(function ($) {
  var ACTIVE_CHECKBOXES = ".field-active input:checkbox";

  $(document.body).delegate(ACTIVE_CHECKBOXES, "change", function () {
    var clicked = this;
    $(ACTIVE_CHECKBOXES).each(function () {
      if (this == clicked) {
        return;
      }

      $(this).removeAttr("checked");
    });
  });

  $("form").bind("submit", function () {
    var actives = $(ACTIVE_CHECKBOXES).filter(":checked").length;

    if (actives !== 1) {
      alert("Please select exactly one active layout instance.");
      return false;
    }
  });
})(django.jQuery);
