

// General data
var data = PHOTO_DATA;
var padding = 10;
var margin = 8;
var padding_top = 30;
var series_category = '';
var current_index = 0;
var icon_height = 39;

// Regexes
var list_regex = /img_li_([\d]+)/;
var photo_regex = /photo_([\d]+)/;
var main_photo_regex = /main_photo_([\d]+)/;

// Keypresses
var LEFT  = 37;
var RIGHT = 39;
var SPACE = 32;
var keypresses = {
    LEFT: false,
    RIGHT: false,
    SPACE: false
};

$(function() {
    $('body').append($('<div/>', {id: 'lightbox-background'}).hide());
    $(window).keydown(keydown_handler).keyup(keyup_handler);
});

function remove_lightbox() {
    if ($(event.target).is('#lightbox-inner-container, #lightbox-inner-container *')) {
        return;
    }
    $('#lightbox-background').fadeOut();
    $('#lightbox-outer-container').fadeOut().promise().done(function(){
        $(this).remove();
    });
}

// This elt is the main image that is clicked
function createLightboxSeries(elt, category) {
    series_category = category;
    var n = main_photo_regex.exec(elt.attr('id'))[1];
    current_index = n;
    var url = elt.parent().attr('href');
    var urls = data[cat_rel[category]];
    var container = $('<div/>', {id: 'lightbox-outer-container'})
        .append($('<div/>', {id: 'lightbox-inner-container'}))
        .css('height', $(document).height());
    container.find('#lightbox-inner-container')
        .css('top', $(window).scrollTop() + padding_top)
        .append($('<div/>', {
            id: 'lightbox-next',
            class: 'nav'
        }))
        .append($('<div/>', {
            id: 'lightbox-prev',
            class: 'nav'
        }));
    container.find('#lightbox-next')
        .append($('<img/>', {src: data.url_root + 'images/lightbox-next.png'}).hide())
        .click(next)
        .mouseenter(function() {
            $(this).find('img').fadeIn();
        })
        .mouseleave(function() {
            $(this).find('img').fadeOut();
        });
    container.find('#lightbox-prev')
        .append($('<img/>', {src: data.url_root + 'images/lightbox-prev.png'}).hide())
        .click(prev)
        .mouseenter(function() {
            $(this).find('img').fadeIn();
        })
        .mouseleave(function() {
            $(this).find('img').fadeOut();
        });;
    container.find('.nav img').css('width', 'auto');

    container.click(remove_lightbox);
    $('body').append(container);
    $('#lightbox-background').fadeIn();

    load_img(url, current_index);
}

var keydown_handler = function(event) {
    if (event.keyCode == RIGHT && !keypresses[RIGHT]) {
        event.preventDefault();
        keypresses[RIGHT] = true;
        next();
    }
    else if (event.keyCode == LEFT && !keypresses[LEFT]) {
        event.preventDefault();
        keypresses[LEFT] = true;
        prev();
    }
    else if (event.keyCode == SPACE && !keypresses[SPACE]) {
        event.preventDefault();
        keypresses[SPACE] = true;
        next();
    }
}

var keyup_handler = function(event) {
    if (event.keyCode == LEFT) {
        keypresses[LEFT] = false;
    }
    else if (event.keyCode == RIGHT) {
        keypresses[RIGHT] = false;
    }
    else if (event.keyCode == SPACE) {
        keypresses[SPACE] = false;
    }
}

function next() {
    if ($('#lightbox-outer-container').length > 0) {
        if (current_index >= data[cat_rel[series_category]].length - 1) {
            return;
        }

        current_index ++;

        $('#lightbox-inner-container > img, #lightbox-inner-container > p')
            .fadeOut().promise().done(function() {
                $(this).remove();
                load_img(data[cat_rel[series_category]][current_index].lightbox_url,
                    current_index);
            });
    }

    next_img();
    return false;
}

function prev() {
    if ($('#lightbox-outer-container').length > 0) {
        if (current_index <= 0) {
            return;
        }

        current_index --;

        $('#lightbox-inner-container > img, #lightbox-inner-container > p')
            .fadeOut().promise().done(function() {
                $(this).remove();
                load_img(data[cat_rel[series_category]][current_index].lightbox_url,
                    current_index);
            });
    }

    prev_img();
    return false;
}

function load_img(url, n) {
    var container = $('#lightbox-outer-container');
    var inner = $('#lightbox-inner-container');

    if (n == 0) {
        $('#lightbox-prev').hide();
    }
    else {
        $('#lightbox-prev').show();
    }

    if (n == data[cat_rel[series_category]].length - 1) {
        $('#lightbox-next').hide();
    }
    else {
        $('#lightbox-next').show();
    }

    $('<img/>', {src: url}).load(function() {
        if (n != current_index) {
            return;
        }

        // inner.stop();
        // inner.find('.nav img').stop();

        var max_width  = window.innerWidth - 2 * padding - 2 * margin;
        // multiply by 0.9 to make room for caption at the bottom
        var max_height = (window.innerHeight - 2 * padding_top - 2 * padding) * 0.9;
        var img_width  = $(this)[0].naturalWidth;
        var img_height = $(this)[0].naturalHeight
        var img_ratio  = img_height / img_width;
        var max_ratio  = max_height / max_width;

        var width  = 0;
        var height = 0;
        var left = 0;

        if (img_ratio < max_ratio) {
            width = Math.min(img_width, max_width);
            height = img_ratio * width;
        }
        else {
            height = Math.min(img_height, max_height);
            width = height / img_ratio;
        }

        left = (window.innerWidth - width - 2 * padding) / 2;

        $(this).css({
            'width': width,
            'height': height
        }).hide();

        inner.prepend($(this));

        var p = $('<p/>', {'width': width})
            .html(data[cat_rel[series_category]][n].caption)
            .hide();
        inner.append(p);
        var inner_height = height + p.height() + parseInt(p.css('margin-top'))
             + parseInt(p.css('margin-bottom'))

        var this_img = $(this);
        var nav_top = (height - icon_height) / 2;

        inner.find('.nav img').animate({
            'margin-top': nav_top
        });

        inner.animate({
            'width' : Math.round(width),
            'height': Math.round(inner_height),
            'left'  : left,
            'top'   : $(window).scrollTop() + padding_top
        },'easeInOutBounce', function() {
            this_img.fadeIn();
            p.fadeIn();
        });

    });
}
