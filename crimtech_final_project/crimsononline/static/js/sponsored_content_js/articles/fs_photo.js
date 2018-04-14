$(document).ready(function() {
    $(".carousel-inner").css('opacity', 0);
    $(".carousel-caption").css('opacity', 0);
    $(".carousel-indicators").css('opacity', 0);
    $(".icon-prev, .icon-next").css('opacity', 0);
    $(".navbar").css('opacity', 0);
	setTimeout(function() {
        $(".carousel-inner").fadeTo(1000, 1);
	}, 800);
    $('.carousel').carousel({
        pause: true,
        interval: false
    });
    setTimeout(function() {
        $(".navbar").fadeTo(1000, 1);
    }, 500);
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
    $("#right-carousel-control").hover(function() {
        $(".at4-share").fadeTo(300, 1);
        $(".at4m-dock").fadeTo(300, 1);
    }, function() {
        $(".at4-share").delay(2000).fadeTo(300, .4);
        $(".at4m-dock").delay(2000).fadeTo(300, .9);
    });
    $(".at-share-btn").hover(function() {
        console.log("test");
    }, function() {
        console.log("test2");
    });
});

function start() {
    $(".lead").fadeToggle(500);
    $(".carousel-caption").fadeTo(1000, 1);
    $(".carousel-indicators").fadeTo(1000, 1);
    $(".icon-prev, .icon-next").fadeTo(1000, 1);
    $(".at4-share").fadeTo(1000, .4);
    $(".at4m-dock").fadeTo(1000, .9);
}
function reset() {
    $(".lead").fadeToggle(500);
    $(".carousel-caption").fadeTo(1000, 0);
    $(".carousel-indicators").fadeTo(1000, 0);
    $(".icon-prev, .icon-next").fadeTo(1000, 0);
    $(".at4-share").fadeTo(1000, 1);
    $(".at4m-dock").fadeTo(1000, 1);
}
