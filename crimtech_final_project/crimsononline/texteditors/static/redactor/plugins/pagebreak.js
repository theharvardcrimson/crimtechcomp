"use strict";

// Page break plugin for Redactor, à la TinyMCE's plugin of the same
// name.

if (!RedactorPlugins) {
  var RedactorPlugins = {};
}

(function () {
  var CSS_CLASS = 'redactor-pagebreak';

  // For legacy reasons, our codebase uses `<!--more-->` to indicate a
  // page break. Comments won't display in Redactor, so we also insert
  // an hr that we can style. (In my tests, the hr and the comment are
  // always deleted together, remarkably.) We make the hr invisible so
  // it doesn't ever leak out by accident; only the editor CSS overrides
  // its style to make it visible.
  var PAGEBREAK_HTML = '<hr class="' + CSS_CLASS + '" style="display: none">' +
                       '<!--more-->';

  RedactorPlugins.pagebreak = function () {
    return {
      insert: function () {
        this.insert.htmlWithoutClean(PAGEBREAK_HTML);
      },

      init: function () {
        var button = this.button.add('pagebreak', 'Page Break');
        this.button.addCallback(button, this.pagebreak.insert);
      }
    }
  }
})();
