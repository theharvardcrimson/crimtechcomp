// CSS triangle :D
var $triangle = $('<div/>', {id: 'triangle', 'class': 'triangle-style'});
var BREAKPOINT = 850; // Where half stories become full width
var MOBILE_BREAK = 520;

var short_size = 200;
var tall_size = 400;
var mobile_tall_size = 275;

var isMobile;

$(document).ready(function() {
    // Social media
    addthis.layers({
        'theme' : 'transparent',
        'share' : {
            'position' : 'right',
            'numPreferredServices' : 5,
            'services': 'facebook, twitter, email, print, more'
        }
    });

    var disqus_shortname = 'thecrimson';
    var dsq = document.createElement('script');
    dsq.type = 'text/javascript';
    dsq.src = 'http://thecrimson.disqus.com/embed.js';
    dsq.async = true;
    (document.getElementsByTagName('head')[0] ||
        document.getElementsByTagName('body')[0]) .appendChild(dsq);

    $('.story').click(function() {
        var $story = $(this);

        // Reset everything
        if ($story.hasClass('selected')) {
            $triangle.hide();
            reset($story);
            find_hidden($story).slideUp();
        }
        else if ($story.hasClass('half'))
            show_half_story($story);
        else
            show_story($story, null);

        window.location.hash = '#' + $story.attr('data-id');
    });

    isMobile = $(window).width() <= 520;

    $(window).on('resize', function() {
        window_change();
    });

    var hash = window.location.hash.replace('#', '');
    if (hash != '') {
        $('div[data-id=' + hash).trigger('click');
    }
});

// Function to show stories that get their own line
function show_story($story, $hidden) {
    if ($hidden == null)
        $hidden = find_hidden($story);

    // Show triangle once other animations complete
    $triangle.hide();
    $story.append($triangle);
    // setTimeout(function() {$triangle.show();}, tall_size);
    $triangle.show();

    // Hide old story, show current story
    reset($('.story.selected'));
    $story.addClass('selected');
    set_height($story, short_size, true);
    $hidden.slideDown();
}

// Function to show stories that share a line with another story
function show_half_story($story) {
    var $story = $story;
    var $other_stories = $story.siblings('.story');
    var $hidden = find_hidden($story);

    // First move story to proper place
    var width = $(window).width();
    if (width <= BREAKPOINT) {
        $story.after($hidden);
        show_story($story, $hidden);
    }
    else {
        $other_stories.parent().append($hidden);

        // Is neighboring story selected?
        if ($other_stories.hasClass('selected')) {
            var $other_hidden = find_hidden($other_stories);

            $other_stories.removeClass('selected');
            $story.addClass('selected');

            $story.append($triangle);
            $other_hidden.hide();
            $hidden.fadeIn();
        }

        // Some other story (or maybe no story) is selected
        else {
            // Same behavior as showing full story
            show_story($story, $hidden);
        }
    }
}

// Reset size, etc. on window size change
function window_change() {
    var width = $(window).width();
    $selected = $('.story.selected');
    $hidden = find_hidden($selected);

    if (width > BREAKPOINT) {
        $selected.parent().append($hidden);
        set_height($selected, short_size,  false);
    }
    else {
        $selected.after($hidden);
        if (width > MOBILE_BREAK) {
            if (!isMobile) { // i.e. WAS not mobile already
                set_height($selected.siblings('.story'), tall_size, false);
            }
            else {
                set_height($('.story').not($selected), tall_size, false);
                isMobile = false;
            }
        }
        else {
            if (isMobile) { // i.e. WAS mobile already
                set_height($selected.siblings('.story'), mobile_tall_size, false);
            }
            else {
                set_height($('.story').not($selected), mobile_tall_size, false);
                isMobile = true;
            }
        }
    }
}

// Unselect the story
function reset($story) {
    $story.removeClass('selected');
    find_hidden($story).slideUp();
    if ($(window).width() > MOBILE_BREAK)
        set_height($story, tall_size, true);
    else
        set_height($story, mobile_tall_size, true);
}

// Animate setting height of story and sibling stories
function set_height($story, h, animate) {
    var width = $(window).width();
    $stories = null;

    if (width > BREAKPOINT)
        $stories = $story.parent().children('.story');
    else
        $stories = $story;

    if (h == short_size)
        $stories.addClass('shrunk');
    else
        $stories.removeClass('shrunk');

    if (animate)
        $stories.animate({height: h}, {queue: false});
    else
        $stories.height(h);


}

// Find the hiddenContent associated with a story div
function find_hidden($story) {
    $content = $story.siblings('.hiddenContent');
    if ($story.hasClass('first'))
        $content = $content.filter('.first');
    if ($story.hasClass('second'))
        $content = $content.filter('.second');

    return $content;
}
