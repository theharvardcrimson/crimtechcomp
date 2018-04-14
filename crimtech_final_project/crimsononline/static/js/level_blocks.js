// Minimum screen width to allow grid to grow to n blocks wide
var limits = {
    6: Number.MAX_VALUE,
    5: 766,
    4: 631,
    3: 501,
    2: 0
};

$(function(){
    level_blocks();
    $(window).resize(function() {
        level_blocks();
    });
});

function level_blocks() {
    var blocks = num_blocks();
    var first = 0;
    var all_elts = $('#block-list li .article-info');
    var row = all_elts.slice(first, first + blocks);
    while (row.length != 0) {
        row.css('height', 'auto');
        var height = max_height(row);
        row.height(height);
        first += blocks;
        row = all_elts.slice(first, first + blocks);
    }
}

function num_blocks() {
    var screen_width = $(window).width();
    var found_blocks = false;
    for (var i = 3; i < 7 && !found_blocks; i ++) {
        if (screen_width < limits[i]) {
            found_blocks = true;
        }
    }

    return i - 2;
}

// From http://stackoverflow.com/questions/6060992/
function max_height(elt) {
    var heights = elt.map(function (){
        return $(this).height();
    }).get();
    return Math.max.apply(null, heights);
}
