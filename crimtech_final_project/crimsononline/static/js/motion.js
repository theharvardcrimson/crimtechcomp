$(document).ready(function() {
  /* Script used for smooth navigation */
  $(".navlink").click(function(event) {
    event.preventDefault();
    var target = $(this).attr("href");
    $("html, body").animate({
      scrollTop: $(target).offset().top - $(".navigation").outerHeight() - 15
    }, 500);
  });

  $("#scroll").click(function() {
    $('html,body').animate({
        scrollTop: $(".content").offset().top},
        'slow');
  });

});



var firstrun = true;
var scenes = [];

/* Resizes elements automatically */
var setElementHeight = function () {
    var height = $(window).height();
    var width = $(window).width();

    // Set up main rel content
    if (width <= 1024) {
      $('#top').css({
        'width' : String(width) + 'px',
        'padding-top' : String($('.navigationwrapper').outerHeight()) + 'px',
      });
    } else {
      $('#top').css({
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

      $('#top').css({
        'background-attachment' : 'scroll',
        'background-position' : '50% ' + String($('.navigationwrapper').outerHeight()) + 'px' ,
      });

    } else {
      $('.shortcodes-image-fullscreen').css({
        'height' : String(height * 0.55) + 'px',
        'width' : String(width) + 'px'
      });

      // Smartphones
      $('#top').css({
        'background-attachment' : 'scroll',
        'background-position' : '50% 0',
      });
    }

    $("#top").height(($(window).height() - parseInt($("#top").css("padding-top"))) * 1.0);
    $("#bgndVideo").height(height);
    // console.log($(window).innerHeight());

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

(function($) {

$(document).ready(function() {

    /* IF YOU WANT TO APPLY SOME BASIC JQUERY TO REMOVE THE VIDEO BACKGROUND ON A SPECIFIC VIEWPORT MANUALLY
*/
     var is_mobile = false;

    if( $('.player').css('display')=='none') {
        is_mobile = true;
    }
    if (is_mobile == true) {
        //Conditional script here
        $('.big-background, .small-background-section').addClass('big-background-default-image');
    }else{
        $(".player").mb_YTPlayer();
    }

    });


    /*  IF YOU WANT TO USE DEVICE.JS TO DETECT THE VIEWPORT AND MANIPULATE THE OUTPUT
        //Device.js will check if it is Tablet or Mobile - http://matthewhudson.me/projects/device.js/
        if (!device.tablet() && !device.mobile()) {
            $(".player").mb_YTPlayer();
        } else {
            //jQuery will add the default background to the preferred class
            $('.big-background, .small-background-section').addClass(
                'big-background-default-image');
        }
    });*/

})(jQuery);
