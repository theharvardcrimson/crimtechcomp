var set_related_content = function(id_prefix, types){
    var p;
    if(id_prefix[0] == '#') { p = id_prefix; }
    else { p = '#' + id_prefix; }
    $(p + '_wrapper .date_input').datepicker();

    var hidden = $(p + '_wrapper input[type="hidden"]');

    // injects a remove button and binds it to remove_content
    var bind_remove = function(ele){
        $('<td style="width: 80px"><a class="button remove" href="#">Remove</a></td>')
            .prependTo(ele)
            .one('click', function(){
                remove_content(ele);
                return false;
            });
    };

    var add_content = function(pk){
        var url = '/admin/content/article/rel_content/get/' + pk + '/';
        $.getJSON(url, function(json){
            // append value to field
            $(hidden).val($(hidden).val() + (pk + ';'));
            // inject into DOM
            json.html = '<tr>' + json.html + '</tr>';
            var target = $(p + '_wrapper .rel_objs');
            bind_remove(
                $(json.html)
                    .appendTo(target)
                    .hide()
                    .data('rel_pk', pk)
                    .fadeTo('normal', 1)
            );
        }, 'html');
    };

    var choose_content = function(){
        add_content($(this).data('rel_pk'));
        $(this)
            .css('cursor', '')
            .css('background-color', '')
            .fadeTo("normal", 0.5)
            .unbind();
    };

    var remove_content = function(ele){
        // remove it from the field
        var id = $(ele).data('rel_pk');
        var vals = $(hidden).val().split(';');
        var str = '';
        for(var i = 0; i < vals.length; i++){
            if(vals[i] && id!=vals[i]){
                str += vals[i] + ';';
            }
        }
        $(hidden).val(str);

        // remove the element
        $(ele).remove()

        // unfade it in the choices area
        $(p + '_wrapper .ajax_search .results tr').each(function(){
            if(id == $(this).data('rel_pk')){
                $(this)
                    .fadeTo('normal', 1)
                    .css('cursor', 'pointer')
                    .one('click', choose_content)
                    .hover(function(){
                        $(this).css('background-color', '#eeeeee');
                    }, function(){
                        $(this).css('background-color', '');
                    });
            }
        });
    };

    // returns true if the content has already been selected
    var already_related = function(pk){
        var id = pk
        var arr = $(hidden).val().split(';')
        for(var i = 0; i < arr.length; i++){
            if(arr[i] && id == arr[i]) return true;
        }
        return false;
    };

    var process_ajax = function(url_base, data){
        // dump results into .results and bind click handlers
        var target = $(p + '_wrapper .ajax_search .results');
        $(target).empty();
        $.each(data.objs, function(){
            var ele = $(this[1]);
            $(ele)
                .appendTo(target)
                .data('rel_pk', this[0])
                .one('click', choose_content)
                .css('cursor', 'pointer')
                .hover(function(){
                    $(this).css('background-color', '#eeeeee');
                }, function(){
                    $(this).css('background-color', '');
                });
            if(already_related(this[0])){
                $(ele)
                    .css('cursor', '')
                    .unbind()
                    .fadeTo('normal', .5);
            }
        });
        if(!data.objs.length){
            $(target).append('<tr><td colspan="5" class="no-results">No Results Found</td></tr>');
        }
        // create paging links
        var p_link = (data.prev_page == 0) ? '' : '<a class="rel-content-pager button" href="#">Prev</a>';
        var n_link = (data.next_page == 0) ? '' : '<a class="rel-content-pager button" href="#">Next</a>';
        target = $(p + '_wrapper .ajax_search .paging_links');
        $(target).empty();
        if(p_link){
            $(p_link)
                .appendTo(target)
                .click(function(){
                    $.getJSON(url_base + '&page=' + data.prev_page , function(data){
                        process_ajax(url_base, data);
                    })
                    return false;
                });
        }
        $(target).append('&nbsp;');
        if(n_link){
            $(n_link)
                .appendTo(target)
                .click(function(){
                    $.getJSON(url_base + '&page=' + data.next_page, function(data){
                        process_ajax(url_base, data);
                    })
                    return false;
                });
        }
    };

    // monkey patch dismiss related lookup popup to do a custom insert
    var originalDismissAddAnotherPopup = dismissAddAnotherPopup;
    dismissAddAnotherPopup = function(win, newId, newRepr){
        var matched = '';
        for(var i = 0; i < types.length; i++){
            if('id_' + types[i] == win.name){
                matched = types[i];
                break;
            }
        }
        if(matched){
            add_content(newId);
            win.close();
        } else {
            return originalDismissAddAnotherPopup(win, newId, newRepr);
        }
    }

    // make rel objs sortable
    $(p + '_wrapper .rel_objs tbody').sortable({stop: function(){
        // reset value of hidden on sort
        $(hidden).val('');
        $(p + '_wrapper .rel_objs tbody tr').each(function(){
            var str = $(this).data('rel_pk')+';';
            $(hidden).val($(hidden).val() + str);
        });
    }});

    // bind remove buttons and attach rel_content data
    var ids = $(hidden).val().split(';');
    $(p + '_wrapper .rel_objs tbody tr').each(function(i){
        id = ids[i].split(',')
        $(this)
            .data('rel_pk', id[0]);
        bind_remove(this);
    });

    // send ajax search request
    $(p + '_go').click(function(){
        var tags = $(p + '_tags').val();
        var start = $(p + '_start_date').val();
        var end = $(p + '_end_date').val();
        var type = $(p + '_type').val().replace(/;/g, '%3B');
        var url = '/admin/content/article/rel_content/find/?ct_id=' + type +
            '&st_dt=' + start + '&end_dt=' + end + '&q=' + tags;

        $.getJSON(url + '&page=1', function(data){
            process_ajax(url, data);
        });
        return false;
    });

    // send ajax request for suggesting related content
    $(p + '_suggest').click(function(){
        var type = $(p + '_type').val();
        var tags = [];
        $('#id_tags_to').find("option").each(function(i){
            tags[i] = $(this).val();
        });
        tagstr = ""
        for(i = 0; i < tags.length; i++){
            if(tagstr != "")
                tagstr = tagstr + ","
            tagstr = tagstr + tags[i]
        }

        var url = '/admin/content/article/rel_content/suggest/' + type + '/' + tagstr + '/1/';
        $.getJSON(url, function(data){
            process_ajax(url.substr(0, url.length - 2), data);
        });
        return false;
    });

};
