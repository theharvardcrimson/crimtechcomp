$(document).ready(function() {
    $("p").each(function(){
        if ($.trim($(this).text()) == ""){
            this.remove();
        }
    });
    $("p:empty").remove();
    $(".headers").after($(".shortcodes-wrapper").first());
    $(".shortcodes-wrapper").first().css({
        'margin-top': '0',
        'width': '100%',
        'padding-bottom': '20px'
    });
    // $(".shortcodes-wrapper").first().after($(".sidebar"));


    $(".navbar").css('opacity', 0);

    setTimeout(function() {
        $(".article-content").removeClass('hide-down');
        $(".article-content").addClass('reveal-up');
    }, 200);
    setTimeout(function() {
        $(".navbar").fadeTo(1000, 1);
    }, 1200);
});
