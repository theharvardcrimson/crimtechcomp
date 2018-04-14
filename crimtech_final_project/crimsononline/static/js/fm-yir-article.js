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

    var update_centers = function(e) {
        $('.roundabout-moveable-item > div').each(function() {
            var top = $(this).parent().height()/2 - $(this).height()/2;
            $(this).css('margin-top', top);
        });
    };

    $('ul#goes-around').roundabout({
        tilt: -23,
        minZ: 100,
        maxZ: 280,
        minOpacity: 0.6,
        minScale: 0.7,
        btnNext: '.goes-around-button',
        triggerFocusEvents: true,
        responsive: true
    }, function() {
        update_centers();

        $('ul#goes-around').on('childrenUpdated', update_centers);
    });

    $('ul#goes-around').on('animationEnd', function(e) {
        var foc = $('ul#goes-around').roundabout('getChildInFocus') + 1;
        var $item = $('ul#goes-around li:nth-child(' + foc + ')');
        $('.goes-around-button div').html($item.attr('data-next') + "  &nbsp;&nbsp;&rarr;");
    });
});
