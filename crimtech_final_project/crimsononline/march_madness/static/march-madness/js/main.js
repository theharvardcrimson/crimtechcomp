$(document).ready(function() {
    $('.story').hover(function(){
        $(this).find('.teaser').stop().animate({'max-height': 200}, 500);
    }, function() {
        var $teaser = $(this).find('.teaser');
        $teaser.stop().css('max-height', $teaser.height()).animate({'max-height': 0}, 500);
    });
});
