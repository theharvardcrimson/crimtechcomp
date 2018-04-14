(function() {
    $(document).ready(function(){
        $('#intro').css('min-height', $(window).height());

        $('#intro .dark-cover').height($('#intro').height());
        $('#intro .intro-text').css('top', $('#intro').height()/(window.INTRO_SCALE_FACTOR || 3.5) - $('#intro .intro-text').height()/2 + 30);
        $('#intro .dark-cover.fader').delay(200).animate({ opacity: 0 }, 3000);

        $('.arrow').delay(3000).fadeIn(1000, function(){
            $(this)
                .css('transition', 'opacity 0.8s')
                .find('img').click(function() {
                    $('html, body').animate({
                        scrollTop: $("#intro").height() - 30
                    }, 1000);
                });
        });

        // Start fancybox

        /* Apply fancybox to multiple items */

        $(".fancybox").fancybox();

        $('.frosh .extra').each(function () {
            var html = $(this).html();
            console.log("HTML", html);
            $(this).html(html.split(":").join(":<br>"));
        });

        $('body:not(.spotlight-light) .frosh').hover(function() {
            var $bi = $(this).find('.bottom-info');
            var $name = $bi.children('.name');
            var $extra = $bi.children('.extra');

            if ($.trim($extra.html())) { // has content
                $name.stop().animate({'top': '100%'});
                $extra.stop().animate({'top': '0'});
            }
        }, function() {
            var $bi = $(this).find('.bottom-info');
            var $name = $bi.children('.name');
            var $extra = $bi.children('.extra');
            $name.stop().animate({'top': '0'}, function() {
                $name.removeAttr('style');
            });
            $extra.stop().animate({'top': '-100%'}, function() {
                $extra.removeAttr('style');
            });
        });
    });
})();
