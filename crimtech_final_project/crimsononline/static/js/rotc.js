$(document).ready(function() {
  /* Script used for smooth navigation */
  $(".navlink").click(function(event) {
    event.preventDefault();
    var target = $(this).attr("href");
    $("html, body").animate({
      scrollTop: $(target).offset().top - $(".navigation").outerHeight() - 15
    }, 500);
  });
});

var firstrun = true;
var scenes = [];

/* Resizes elements automatically */
var setElementHeight = function () {
    var height = $(window).height() * 0.9;
    var width = $(window).width();

    // Set up main rel content
    if (width <= 1024) {
      $('.intro.image').css({
        'width' : String(width) + 'px',
        'padding-top' : String($('.navigationwrapper').outerHeight()) + 'px',
      });
    } else {
      $('.intro.image').css({
        'width' : String(width) + 'px',
        'padding-top' : String($('.navigationwrapper').outerHeight() + height/4) + 'px',
      });
    }

    // Set up large pictures depending on device
    if(width > 600) {
      // Desktop and tablets
      $('.shortcodes-image-fullscreen').css({
        'height' : String(height) + 'px',
        'width' : String(width) + 'px'
      });

      $('.intro.image').css({
        'background-attachment' : 'scroll',
        'background-position' : '50% ' + String($('.navigationwrapper').outerHeight()) + 'px' ,
      });

    } else {
      $('.shortcodes-image-fullscreen').css({
        'height' : String(height * 0.55) + 'px',
        'width' : String(width) + 'px'
      });

      // Smartphones
      $('.intro.image').css({
        'background-attachment' : 'scroll',
        'background-position' : '50% 0',
      });
    }

    $("#top.image").height(($(window).height() - parseInt($("#top").css("padding-top"))) * 0.8);
};

$(window).on("resize", function () {
    setElementHeight();
}).resize();

$(function () {
  setElementHeight();

  // Move image bylines after description.
  //
  // XXX figure out how to have different shortcodes templates for different
  // article templates, or make shortcodes more flexibile.
  $(".shortcodes-byline + .shortcodes-description").each(function () {
    $(this).prev().detach().appendTo($(this));
  });

  $(".shortcodes-byline")
    .not(".shortcodes-description .shortcodes-byline")
    .each(function () {
      $(this).wrap("<div class='shortcodes-description'></div>");
    });
});

youtubeVideoHandlers = [];

function onYouTubeIframeAPIReady(playerId) {
  youtubeVideoHandlers.forEach(function (handler) {
    handler();
  });
}
