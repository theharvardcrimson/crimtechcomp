$(document).ready(function() {
    $('#intro').css('min-height', $(window).height());
    $('#intro .dark-cover').height($('#intro').height());
    $('#intro .intro-text').css('top', $('#intro').height()/2.5 - $('#intro .intro-text').height()/2);
    $('#intro .dark-cover.fader').delay(200).animate({'opacity': 0}, 5000);

    $('#view-button').delay(3000).fadeTo(1000, 1);
    $('#view-button a').click(function(e) {
        e.preventDefault();
        $('html, body').animate({scrollTop: $("#intro").height()}, 1000);
    }).delay(3000).fadeTo(1000, 1);
    $('.header-nav a:not(:first-child)').click(function(e) {
        e.preventDefault();
        var target = $(this).attr("href");
        $("html, body").animate({
            scrollTop: $(target).offset().top - $("header").outerHeight() + 15
        }, 500);
    }).delay(3000).fadeTo(1000, 1);

    $('.yip-link').magnificPopup({
        type: 'image',
        image: {
            verticalFit: true,
            titleSrc: 'data-caption'
        },
        gallery:{enabled:true}
    });
});

var controller;
$(document).ready(function($) {
    controller = new ScrollMagic();

    $(".overheard-wrapper").each(function(index, element) {
        var $quote = $(element).children('.overheard-quote');
        var tween;
        if ($(element).hasClass('oh-quote-right'))
            tween = TweenMax.to($quote, 1.5, {opacity: 1, right: 0, ease: Cubic.easeOut});
        else
            tween = TweenMax.to($quote, 1.5, {opacity: 1, left: 0, ease: Cubic.easeOut});
        var scene = new ScrollScene({triggerElement: $quote.children('.overheard-quote-trigger')})
                        .setTween(tween)
                        .addTo(controller);
    });
});
