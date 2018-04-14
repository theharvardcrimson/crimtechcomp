// functions for media viewer page
$(document).ready(function(){
    var _media_cache = {};
    var _page_cache = {};
    var _cur_sort = "recent";
    var _cur_section = "all";
    var _cur_type = "all";
    var _filter_state = 0;

    // sort/filter buttons
    // TODO: add filtering
    // TODO: destroy page cache when switching ordering

    function inject_sidebar(page_num, sortby, section, type){
        var inject_results = function(results){
            $("#viewer_sidebar #sidebar_galleries").fadeOut('fast', function(){
                $("#viewer_sidebar #sidebar_galleries").empty()
                    .append($(results))
                    .fadeIn('fast')
            });
        };

        ajax = $.get('/section/media/', {ajax: '', sort: sortby,
            page:page_num, section: section, type: type} , inject_results);
    }

    // sorting
    $("#sort_filters a").live("click", function(e){
        var sortby = $(this).attr("href");
        _cur_sort = sortby;

        $('#sort_filters a').find('span').removeClass("thclabel_redtive");
        $('#sort_filters a').find('span').addClass("thclabel_red");
        $(this).find('span').removeClass("thclabel_red");
        $(this).find('span').addClass("thclabel_redtive");

        inject_sidebar(1, _cur_sort, _cur_section, _cur_type);

        return false;
    });

    // filtering by section
    $("#section_filters a").live("click", function(e){
        var section = $(this).attr("href");

        // section needs to be added
        if(_cur_section != section){
            $("#section_filters a").find('span').addClass("thclabel_red");
            $("#section_filters a").find('span').removeClass("thclabel_redtive");
            $(this).find('span').removeClass("thclabel_red");
            $(this).find('span').addClass("thclabel_redtive");
            _cur_section = section;
        }

        inject_sidebar(1, _cur_sort, _cur_section, _cur_type);

        return false;
    });

    // filtering by type
    $("#type_filters a").live("click", function(e){
        var type = $(this).attr("href");

        // section needs to be added
        if(_cur_type != type){
            $("#type_filters a").find('span').addClass("thclabel_red");
            $("#type_filters a").find('span').removeClass("thclabel_redtive");
            $(this).find('span').removeClass("thclabel_red");
            $(this).find('span').addClass("thclabel_redtive");
            _cur_type = type;
        }

        inject_sidebar(1, _cur_sort, _cur_section, _cur_type);

        return false;
    });

    // toggle filters
    $("span#toggle_filters").live("click", function(e){
        if(_filter_state){
            $("#filter_spans").slideUp("slow");
            $(this).text("Filter");
        }
        else{
            $("#filter_spans").slideDown("slow");
            $(this).text("Hide Filters");
        }
        _filter_state = 1-_filter_state
    });

    // pagination buttons
    $(".pagination a").live("click", function(e){
        var page_num = $(this).attr("href").split("#")[1];

        /*
        // look for the object in the cache, fallback on ajax
        if(_page_cache.hasOwnProperty(page_num)){
            inject_results(_media_cache[page_num]);
        } else {
            $.get('/section/media/', {page: page_num, ajax:''}, inject_results, function(html){
                _page_cache[page_num] = html;
                inject_results(html);
            }, 'html');
        }*/

        inject_sidebar(page_num, _cur_sort, _cur_section, _cur_type);

        return false;
    });

    // loading media from the sidebar
    $("#viewer_sidebar ul a").live("click", function(e){
        // where to load the resource from
        var url = $(this).attr("href");

        // destroy the old object in the viewer area and add the new item
        var inject_results = function(results){
            $("#viewer_main").fadeOut('fast', function(){
            $("#viewer_main").empty().append($(results)).fadeIn('fast');
        })};

        // look for the object in the cache, fallback on ajax
        if(_media_cache.hasOwnProperty(url)){
            inject_results(_media_cache[url]);
        } else {
            $.get(url, {render:'media_viewer'}, function(html){
                _media_cache[url] = html;
                inject_results(html);
            }, 'html');
        }

        // make active gallery highlight
        $("#viewer_sidebar").find("li.active").removeClass("active");
        $(this).parent().parent().addClass("active");

        return false;
    });
});
