var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-327124-1']);
_gaq.push(['_setDomainName', 'thecrimson.com']);
_gaq.push(['_trackPageview']);

(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();

$(document).ready(function() {
  /* Script used for smooth navigation */
  $(".navlink").click(function(event) {
    event.preventDefault();
    var target = $(this).attr("href")
    $("html, body").animate({
      scrollTop: $(target).offset().top - $(".navigation").outerHeight() - 15
    }, 500);
  });
});

var controller;
var firstrun = true;
var __PARALLAX_DURATION__ = 500;
var scenes = [];
var controller_init = false;

$(document).ready(function($) {

  // CSS needs exact pixels for scroll magic to work well with resizing
  var height = $(window).height();
  var width = $(window).width();


  // Set up main rel content
  if (width <= 1024) {
    $('.intro').css({
      'width' : String(width) + 'px',
      'padding-top' : String($('.navigationwrapper').outerHeight()) + 'px',
    });
  } else {
    $('.intro').css({
      'width' : String(width) + 'px',
      'padding-top' : String($('.navigationwrapper').outerHeight() + height/8) + 'px',
    });
  }

  // Set up large pictures depending on device
  if(width > 600) {
    $('.intro').css({
      'background-attachment' : 'fixed',
      'background-position' : '50% ' + String($('.navigationwrapper').outerHeight()) + 'px' ,
    });
  } else {
    $('.intro').css({
      'background-attachment' : 'scroll',
      'background-position' : '50% '+ String($('.navigationwrapper').outerHeight()) + 'px',
    });
  }

  $("#top").height($(window).height() - parseInt($("#top").css("padding-top")));

  // Set up parallax controller for non-mobile devices
  if(width > 600) {
    controller_init = true;
    controller = new ScrollMagic({vertical: true});

    // Build timelines
    $(".shortcodes-wrapper-fullscreen").each(function(index, element) {
      var $container = $(element).children('.shortcodes-object-fullscreen');
      var $background = $container.children('.shortcodes-image-fullscreen');
      var $quote = $background.children('.shortcodes-caption-fullscreen');

      // build tween
      var tween = new TimelineMax ()
        .add([
          TweenMax.fromTo($quote, 1, {y: "750%", ease: Linear.easeNone}, {y: "-750%", ease: Linear.easeNone}),
          TweenMax.fromTo($background, 1, {backgroundPosition: "50% 0", ease: Linear.easeNone}, {backgroundPosition: "50% -100px", ease: Linear.easeNone}),
        ]);

      // build scene
      var scene = new ScrollScene({triggerElement: $container, duration: __PARALLAX_DURATION__, offset: height/2})
          .setTween(tween)
          .setPin($container)
          .addTo(controller);
      scenes.push(scene);
    });
  }
});


/* Resizes elements automatically */
var setElementHeight = function () {
    var height = $(window).height();
    var width = $(window).width();

    if(width > 600 && !controller_init) {
      controller_init = true;
      firstrun = false
      controller = new ScrollMagic({vertical: true});

      // Build timelines
      $(".shortcodes-wrapper-fullscreen").each(function(index, element) {
        var $container = $(element).children('.shortcodes-object-fullscreen');
        var $background = $container.children('.shortcodes-image-fullscreen');
        var $quote = $background.children('.shortcodes-caption-fullscreen');

        // build tween
        var tween = new TimelineMax ()
          .add([
            TweenMax.fromTo($quote, 1, {y: "750%", ease: Linear.easeNone}, {y: "-750%", ease: Linear.easeNone}),
            TweenMax.fromTo($background, 1, {backgroundPosition: "50% 0%", ease: Linear.easeNone}, {backgroundPosition: "50% 50%", ease: Linear.easeNone}),
          ]);

        // build scene
        var scene = new ScrollScene({triggerElement: $container, duration: __PARALLAX_DURATION__, offset: height/2})
            .setTween(tween)
            .setPin($container)
            .addTo(controller);
        scenes.push(scene);
      });

    } else if(firstrun && controller_init) {
      firstrun = false;
    } else if(width <= 600) {
      if(controller_init) {

        controller_init = false;
        controller.destroy(true);

        while(scenes.length > 0)
          scenes.pop();

        // Reset original positions
        $(".shortcodes-wrapper-fullscreen").each(function(index, element) {
          var $container = $(element).children('.shortcodes-object-fullscreen');
          var $background = $container.children('.shortcodes-image-fullscreen');
          var $quote = $background.children('.shortcodes-caption-fullscreen');

          $quote.css({
            '-webkit-transform' : '',
          });
        });

      }


    } else {
      var arrayLength = scenes.length;
      for (var i = 0; i < arrayLength; i++) {
        scenes[i].offset(height/2);
      }
    }

    // Set up main rel content
    if (width <= 1024) {
      $('.intro').css({
        'width' : String(width) + 'px',
        'padding-top' : String($('.navigationwrapper').outerHeight()) + 'px',
      });
    } else {
      $('.intro').css({
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

      $('.intro').css({
        'background-attachment' : 'fixed',
        'background-position' : '50% ' + String($('.navigationwrapper').outerHeight()) + 'px' ,
      });

    } else {
      // Smartphones
      $('.intro').css({
        'background-attachment' : 'scroll',
        'background-position' : '50% 0',
      });
    }

    $("#top").height($(window).height() - parseInt($("#top").css("padding-top")));

    // Fixes specifically for parallax / scroll magic resize (kinda [very] janky)
    $('.shortcodes-object-fullscreen').css({
      'width' : String(width) + 'px',
    });
    $('.shortcodes-image-fullscreen').css({
      'width' : String(width) + 'px',
      'height' : 'auto',
    });
    $('.scrollmagic-pin-spacer').css({
      'margin-left' : '0px',
      'margin-left' : '0px',
    });
}

$(window).on("resize", function () {
    setElementHeight();
}).resize();
