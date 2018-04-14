$(document).ready(function() {
	$(".lead-fs").css('opacity', 0);
	$(".headers").css('opacity', 0);
	setTimeout(function() {
        $(".lead-fs").fadeTo(1000, 1);
	}, 200);
    setTimeout(function() {
        $(".headers").fadeTo(1000, 1);
    }, 1200);
    setTimeout(function() {
        $(".navbar").fadeTo(1000, 1);
    }, 2200);
    setTimeout(function() {
        $.getScript('//s7.addthis.com/js/300/addthis_widget.js#pubid=thecrimson', function() {
            addthis.layers({
                'theme' : 'transparent',
                'share' : {
                  'position' : 'right',
                  'numPreferredServices' : 5
                }
            });
        });
    }, 500);
	var actions = new Waypoint({
        element: document.getElementById('headers'),
        handler: function(direction) {
            if (direction == 'down') {
                $(".addthis-smartlayers").fadeTo(1000, 1);
                $('.article-body').removeClass('hide-down');
                $('.article-body').addClass('reveal-up');
            }
            if (direction == 'up') {
                $(".addthis-smartlayers").fadeTo(1000, .2);
                $('.article-body').removeClass('reveal-up');
                $('.article-body').addClass('hide-down');
            }
        },
        offset: '15%'
    });
});
