// Basic Page Functionality JavaScript

(function($) {
    "use strict"; // Start of use strict

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a').click(function(){
            $('.navbar-toggle:visible').click();
    });

    // Offset for Main Navigation
    $('#mainNav').affix({
        offset: {
            top: 100
        }
    })

})(jQuery); // End of use strict

// jQuery for page scrolling feature - requires jQuery Easing plugin
function bindPageScroll(s) {
    $(s).bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top + 15)
        }, 2000, 'easeInOutExpo');
        event.preventDefault();
    });
}
var fs_vid_ratio = 1.77;
function resize_fs_video(s) {
    var w = $(window).width();
    var h = $(window).height();
    if (w > h * fs_vid_ratio) {
        $(s).css({
            'height': w / fs_vid_ratio,
            'width': w,
        });
    }
    else {
        $(s).css({
            'height': h,
            'width': h * 1.78,
        });
    }
}
function reveal(id, delay) {
    setTimeout(function() {
        $(id).removeClass('hide');
        $(id).addClass('reveal');
    }, delay);
}
function hide(id, delay) {
    setTimeout(function() {
        $(id).removeClass('reveal');
        $(id).addClass('hide');
    }, delay);
}
function checkNavbarToggle() {
    if ($('.navbar-collapse').hasClass('in')) {
        $("button.navbar-toggle").click();
    }
}
function isVisible(element) {
    var windowHeight = $(window).height();
    var windowScrollTop = $(window).scrollTop();
    var elementHeight = $(element).height();
    var elementOffsetTop = $(element).offset().top;

    return ((elementOffsetTop <= windowScrollTop + windowHeight) && (elementOffsetTop + elementHeight >= windowScrollTop));
}
$(document).click(function(event) {
    var clickover = $(event.target);
    var $navbar = $(".navbar-collapse");
    var _opened = $navbar.hasClass("in");
    if (_opened === true && !clickover.hasClass("navbar-toggle")) {
        $navbar.collapse('hide');
    }
});
