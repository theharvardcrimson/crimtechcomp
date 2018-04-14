// PHOTO_DATA comes from data.js or django-generated JSON
var data = PHOTO_DATA;

// Global variable so lightbox has access to it - in the future, should be
// passed to a lightbox object
cat_rel = {
    "The Year in Photos" : "The Year in Photos",
    "Boston Marathon"    : "Year in Photos - Boston Marathon Bombing",
    "Breaking News"      : "Year in Photos - Breaking News",
    "Sports"             : "Year in Photos - Sports",
    "Fifteen Minutes"    : "Year in Photos - Fifteen Minutes",
    "Campus Life"        : "Year in Photos - Campus Life",
    "Arts"               : "Year in Photos - Arts"
}

var current_category = '';
// Rexeges
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
    click_section($('#sections li:first-child a'));

    $('#sections li a').click(function() {
        event.preventDefault();
        click_section($(this));
    });
});

// elt should be an element matching
// $('#current-photo .main-photo-container a img')
function gen_lightbox(elt) {
    createLightboxSeries(elt, current_category);
}

// elt should be an element matching $('#sections li a')
function click_section(elt) {
    if (elt.hasClass('active')) {
        return;
    }
    $('#sections li a.active').removeClass('active');
    elt.addClass('active');
    fill_gallery(elt.html());
}

// elt should be an element matching $('#photos li .photo-container.current')
function click_thumbnail(elt) {
    if (elt.hasClass('current')) {
        return;
    }

    // Loading...
    $('#current-photo img, #current-photo p').fadeOut().promise().done(function() {
        $('#current-photo img').attr('src', data.url_root + 'images/photo_loading.gif').fadeIn();
    });

    $('.current').removeClass('current');
    elt.addClass('current');
    var current_li = elt.parent();
    var n = list_regex.exec(current_li.attr('id'))[1];
    var category = current_category;
    var image = $('<img/>').attr({
        'src': data[cat_rel[current_category]][n].med_url,
        'id': 'main_photo_' + n
    }).load(function() {
        if (category != current_category) {
            return;
        }

        var current_active_index = list_regex.exec($('.current').parent()
            .attr('id'))[1];
        if (n != current_active_index) {
            return;
        }

        var new_div = $('<div/>', {class: 'main-photo-container'})
            .append($('<a/>', {
                class: 'lightbox',
                href: data[cat_rel[current_category]][current_active_index].lightbox_url
            }).append($(this))).append($('<p/>').html(data[cat_rel[current_category]][current_active_index].caption)).hide();

        new_div.find('a').click(function() {
            event.preventDefault();
            gen_lightbox($(this).find('img'));
        });

        $('#current-photo').html('');
        $('#current-photo').append(new_div);
        new_div.fadeIn();
    });
}

// category is a string
function fill_gallery(category) {
    // validate category
    if (category == current_category || !data.hasOwnProperty(cat_rel[category])) {
        return;
    }
    console.log(data[cat_rel[category]]);
    current_category = category;

    // Clear HTML in galleries
    $('#photos').html('');
    $("#current-photo img, #current-photo p").fadeOut();

    for (var i = 0; i < data[cat_rel[category]].length; i++) {
        var empty_item = $('<li/>', {id: 'img_li_' + i})
            .append($('<div/>', {class: 'photo-container'})
            .append($('<img/>', {
                'src': data.url_root + 'images/photo_loading.gif'
            })));

        empty_item.find('img').css('margin-top', 49);

        if (category == 'Breaking News' && i > 4) {
            empty_item.addClass('small-thumb');
        }
        $("#photos").append(empty_item);
    }

    // Fill photo list
    var urls = data[cat_rel[category]];
    for (var i = 0; i < data[cat_rel[category]].length; i ++) {
        $('<img/>').attr('src', urls[i].thumb_url).attr('id', 'photo_' + i).load(function() {
            if (current_category != category) {
                return;
            }

            $(this).hide();

            var n = photo_regex.exec($(this).attr('id'))[1];
            $('#img_li_' + n + ' .photo-container img').remove();
            $('#img_li_' + n + ' .photo-container').append($(this));

            $(this).fadeIn();

            $(this).parent().mouseup(function() {
                click_thumbnail($(this));
            });

            if (n == 0) {
                click_thumbnail($(this).parent());
            }
        });
    }
}

// Global so that year-in-photo-lightbox-cust.js can access them
next_img = function() {
    var current_active_index = parseInt(list_regex.exec($('.current').parent()
            .attr('id'))[1]);
    if (current_active_index >= data[cat_rel[current_category]].length - 1) {
        return;
    }

    // Add one to increment, add another because CSS selectors are 1-indexed
    var n = current_active_index + 2;
    click_thumbnail($('#photos li:nth-child(' + n + ') .photo-container'));
}

// Global so that year-in-photo-lightbox-cust.js can access them
prev_img = function() {
    var current_active_index = parseInt(list_regex.exec($('.current').parent()
            .attr('id'))[1]);
    if (current_active_index <= 0) {
        return;
    }

    // Subtract one to decrement, add one because CSS selectors are 1-indexed
    var n = current_active_index;
    click_thumbnail($('#photos li:nth-child(' + n + ') .photo-container'));
}
