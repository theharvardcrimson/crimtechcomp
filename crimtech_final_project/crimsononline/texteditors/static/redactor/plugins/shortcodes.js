"use strict";

// crimsononline.shortcode formatting plugin for Redactor.

if (!RedactorPlugins) {
  var RedactorPlugins = {};
}

(function ($) {
  var CSS_CLASS = 'redactor-shortcode';
  var SHORTCODE_REGEX = /{[^}]+}/g;
  var CLEAN_REGEX = new RegExp('<span class="' + CSS_CLASS + '">(.*?)</span>',
                               'gi');

  // Due to DOM API idosyncracies, constructing a Range object requires
  // specifying the endpoints relative to the innermost element's start.
  // For example, given the following DOM
  //
  // <p>
  //     That's how     --
  //     <em>you</em>    | range
  //     get ants.      --
  // </p>
  //
  // the range containing "how <em>you</em> get" has a start endpoint
  // relative to to the "That's how" text node, and an end endpoint
  // relative to "get ants." But to perform regex matching, the text
  // contents must be one continuous, HTML-free string, "That's how you
  // get ants."
  //
  // So a TextTree walks the DOM to construct the continuous, HTML-free
  // string in `TextTree#contents`, while internally remembering which
  // DOM node each character is stored in. Then, `TextTree#getRange`
  // will construct a Range object using start and end offsets relative
  // to the beginning of `TextTree#contents`.
  function TextTree(element) {
    if (element instanceof $) {
      element = element[0];
    }

    this.strings = [];

    var offset = 0;
    var treeWalker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
    while (treeWalker.nextNode()) {
      this.strings.push({
        offset: offset,
        node: treeWalker.currentNode,
      });
      offset += treeWalker.currentNode.length;
    };

    this.contents = this.strings.map(function (string) {
      return string.node.data;
    }).join("");
  }

  TextTree.prototype.getRange = function (startOffset, endOffset) {
    var i = 0;
    var range = document.createRange();

    // Start offsets greedily advance (>=) to the next node when
    // possible.
    while (startOffset >= this.strings[i].offset + this.strings[i].node.length) {
      i++;
    }
    range.setStart(this.strings[i].node, startOffset - this.strings[i].offset);

    // End offsets conservatively stay within the current node (>) when
    // possible.
    while (endOffset > this.strings[i].offset + this.strings[i].node.length) {
      i++;
    }
    range.setEnd(this.strings[i].node, endOffset - this.strings[i].offset);

    return range;
  }


  // Search the contents of `element` for any text that looks like a
  // shortcode and return a Range object containing the shortcode.
  function grepElement(element, regex) {
    // RegExp#exec modifies the regex's internal state, so make a copy.
    regex = new RegExp(regex);

    var match;
    var ranges = [];
    var textTree = new TextTree(element);

    while ((match = regex.exec(textTree.contents)) !== null) {
      var startOffset = match.index;
      var endOffset = match.index + match[0].length;
      ranges.push(textTree.getRange(startOffset, endOffset));
    }

    return ranges;
  }


  RedactorPlugins.shortcodes = function () {
    return {
      // Wrap all shortcodes in an element with CSS_CLASS applied.
      format: function () {
        this.selection.save();

        // Remove existing wrapper elements for idempotency.
        this.$editor.find('.' + CSS_CLASS).contents().unwrap();

        grepElement(this.$editor, SHORTCODE_REGEX).forEach(function (range) {
          var wrapper = document.createElement("span");
          wrapper.className = CSS_CLASS;

          try {
            range.surroundContents(wrapper);
          } catch (ex) {
            // Bad boundary points errors occur when the range spans two
            // or more non-text nodes. Ignore these; they're usually the
            // result of a partially-typed shortcode that won't be
            // considered a shortcode by the Python parser anyway.
            if (ex.name !== "BAD_BOUNDARYPOINTS_ERR" &&  // DOM Level 2
                ex.name !== "InvalidStateError") {       // DOM4
              console.log(ex);
            }
          }
        });

        this.selection.restore();
      },

      // Strip our HTML wrappers so they don't appear in the final
      // output.
      clean: function (html) {
        // Yes, HTML isn't a regular langauge. But Redactor internals do
        // this all over the place, so YOLO.
        return html.replace(CLEAN_REGEX, '$1');
      },

      init: function () {
        // Redactor doesn't provide a syncBefore hook for plugins;
        // monkey-patch the end-user configuration option, but preserve
        // whatever callback the user specified, if any.
        //
        // The syncBefore callback can modify the HTML displayed in the
        // visual WYSIWYG editor is synced with the backing textarea
        // that's actually saved to the database.
        var oldSyncBeforeCallback = this.opts.oldSyncBeforeCallback;
        this.opts.syncBeforeCallback = function (html) {
          if (oldSyncBeforeCallback && $.isFunction(oldSyncBeforeCallback)) {
            html = oldSyncBeforeCallback(html);
          }

          return this.shortcodes.clean(html);
        }

        // Format on keypress.
        this.$editor.on('keyup.redactor-limiter',
                        this.shortcodes.format.bind(this));


        // Format once at start.
        this.shortcodes.format();
      }
    }
  }
})(jQuery);
