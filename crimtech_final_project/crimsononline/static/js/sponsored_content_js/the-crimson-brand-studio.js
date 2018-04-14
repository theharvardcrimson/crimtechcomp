$(document).ready(function() {
    // $(".navbar").css('opacity', '0');
    var landing_video = new Vimeo.Player($("#landing-video"));
    var landing_video_success = false;
    bindPageScroll('a.page-scroll');
    window.onload = function() {
        var isMobile = (('ontouchstart' in window) || (navigator.msMaxTouchPoints > 0));
        console.log(isMobile);
        resize_fs_video('#landing-video');
        resize_fs_video('#landing-video-backup');
        $(window).resize(function() {
            resize_fs_video('#landing-video');
            resize_fs_video('#landing-video-backup');
        });

        $("#page-hide").fadeOut("slow");
        setTimeout(function() {
            $(".intro-lead-in").fadeTo(1000, 1);
        }, 1500);
        setTimeout(function() {
            $("#btn1").fadeTo(1000, 1);
        }, 2800);
        setTimeout(function() {
            $("#btn2").fadeTo(1000, 1);
        }, 3000);
        setTimeout(function() {
            $("#btn3").fadeTo(1000, 1);
        }, 3200);
        setTimeout(function() {
            $("#to_about").fadeTo(1000, 1);
        }, 3200);
        landing_video.ready().then(function() {
            landing_video.play();
            if ($(window).scrollTop() > $(window).height()) {
                landing_video.pause();
            }
            var callback = function(data) {
                // console.log(data);
                // if the video hasn't played more than 0.2s, let's assume that
                // your connection isn't good enough for the video
                if (data.percent > 0.2) {
                    // console.log('video ready :)')
                    landing_video_success = true;
                    landing_video.getPaused().then(function(paused) {
                        if (paused) {
                            landing_video.play();
                        }
                    });
                    $("#landing-video-backup").fadeOut("slow");
                }
                else {
                    // console.log('video not ready :(');
                    if (!paused) {
                            landing_video.pause();
                    }
                }
                setTimeout(function() { $("#page-hide").fadeOut("slow"); }, 500);
            }
            setTimeout(function() {
                landing_video.on('progress', function(data) {
                    callback(data);
                });
                landing_video.off('progress', callback);
            }, 0.500);
        });
        var navbar = new Waypoint({
            element: document.getElementById('about'),
            handler: function(direction) {
                if (direction == 'down') {
                    $(".navbar").fadeTo(1000, 1);
                    checkNavbarToggle();
                }
                if (direction == 'up') {
                    $(".navbar").fadeTo(1000, 0);
                    checkNavbarToggle();
                }
            }
        });

        var rm_grayscale = new Waypoint({
            element: document.getElementById('tagline'),
            handler: function(direction) {
                if (direction == 'down') {
                    $('#landing-video').removeClass("grayscale");
                    $('#landing-video-backup').removeClass("grayscale");
                    $('#landing-video').addClass("colorize");
                    $('#landing-video-backup').addClass("colorize");
                }
                if (direction == 'up') {
                    $('#landing-video').removeClass("colorize");
                    $('#landing-video-backup').removeClass("colorize");
                    $('#landing-video').addClass("grayscale");
                    $('#landing-video-backup').addClass("grayscale");
                }
            }
        });

        var saver = new Waypoint({
            element: document.getElementById('about'),
            handler: function(direction) {
                if (direction == 'down') {
                    if (!landing_video_success) {
                        $("#landing-video-backup").hide();
                    }
                    landing_video.pause();
                    $('#landing-video').hide();
                }
                if (direction == 'up') {
                    if (!landing_video_success) {
                        $("#landing-video-backup").show();
                    }
                    landing_video.play();
                    $('#landing-video').show();
                }
            }
        });
        var about_section_reveal = new Waypoint({
            element: document.getElementById('about_section-trigger'),
            handler: function(direction) {
                if (direction == 'down') {
                    $('#about h2, #about_text').removeClass('hide-down');
                    $('#about h2, #about_text').addClass('reveal-up');
                }
                if (direction == 'up') {
                    $('#about h2, #about_text').removeClass('reveal-up');
                    $('#about h2, #about_text').addClass('hide-down');
                }
            }
        });
        var what_section_reveal = new Waypoint({
            element: document.getElementById('what_section-trigger'),
            handler: function(direction) {
                if (direction == 'down') {
                    $('#what h2, #what-icons').removeClass('hide-down');
                    $('#what h2, #what-icons').addClass('reveal-up');
                    reveal('#photography', 600);
                    reveal('#videography', 700);
                    reveal('#outreach', 800);
                    reveal('#design', 900);
                    reveal('#analytics', 1000);
                    reveal('#code', 1100);
                }
                if (direction == 'up') {
                    $('#what h2, #what-icons').removeClass('reveal-up');
                    $('#what h2, #what-icons').addClass('hide-down');
                    hide('#videography', 0);
                    hide('#photography', 0);
                    hide('#outreach', 0);
                    hide('#design', 0);
                    hide('#analytics', 0);
                    hide('#code', 0);
                }
            }
        });
        var next_section_element = 'what';
        if (isMobile) { next_section_element = 'what-mobile-trigger'; }
        var next_section = new Waypoint({
            element: document.getElementById(next_section_element),
            handler: function(direction) {
                if (direction == 'down') {
                    $('#mid-fs-pic').hide();
                }
                if (direction == 'up') {
                    $('#mid-fs-pic').show();
                }
            }
        });
        var contact_section_reveal = new Waypoint({
            element: document.getElementById('contact'),
            handler: function(direction) {
                if (direction == 'down') {
                    setTimeout(function() {
                        $('#contact-text').removeClass('hide-down');
                        $('#contact-text').addClass('reveal-up');
                    }, 200);
                }
                if (direction == 'up') {
                    $('#contact-text').removeClass('reveal-up');
                    $('#contact-text').addClass('hide-down');
                }
            },
            offset: 'bottom-in-view'
        });
    }

});
