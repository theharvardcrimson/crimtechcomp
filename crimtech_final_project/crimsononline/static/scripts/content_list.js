// redirect if anchor in url
if(window.location.hash){window.location = window.location.hash.substring(1,window.location.hash.length-1);}


$(document).ready(function(){
    var inject_results = function(results){
        $("#filter_toggle_contents").empty().append(results.content_filters);
        $(".content_list_content").fadeOut('fast', function(){
            $(this).empty()
                .append(results.content_list)
                .fadeIn('fast')
        });
    };

    // Pagination buttons
    $(".pagination a").live("click", function(e){
        ajax = $.getJSON($(this).attr('href') + "?ajax", inject_results);
        window.location.hash = $(this).attr('href')
        return false;
    });

    // Filter checkboxes
    $("#filter_toggle_contents input").live("click", function(e){
        ajax = $.getJSON($(this).val() + "?ajax", inject_results);
        window.location.hash = $(this).val()
        return false;
    });

    // Filter sliding effects
    $("a#filter_toggle").click(function () {
        if ($("#filter_toggle_contents").is(":hidden")) {
            $("#filter_toggle_contents").slideDown("slow");
            $(this).text("Hide Filters");
        } else {
            $("#filter_toggle_contents").slideUp("slow");
            $(this).text("Filter");
        }
    });

});
