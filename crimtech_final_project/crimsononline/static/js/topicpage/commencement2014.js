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
