var set_search_choice_field = function(id_prefix, ajax_url){

    var p;  // prefix of all important elements in question
    if(id_prefix[0] == '#') { p = id_prefix; }
    else { p = '#' + id_prefix; }

    // set datepickers on date picking items
    $(p + '_wrapper .date_input').datepicker();

    // the field where all the values go
    var hidden = $(p + '_wrapper input[type="hidden"]');

    // injects a remove button and binds it to remove_object
    var bind_remove = function(ele){
        $('<a class="button remove" href="#">Remove</a>')
            .prependTo(ele)
            .one('click', function(){
                remove_object(ele);
                return false;
            });
    };

    // adds the item to the selected items list
    //   also
    var add_object = function(ele){
        var target = $(p + '_wrapper .chosen_objs');
        var pk = $(ele).data('pk')
        // append value to field
        var cur_val = $(hidden).val()
        if(!cur_val){
            $(hidden).val(pk);
            target.empty();
        } else {
            $(hidden).val(cur_val + ',' + pk);
        }
        // inject into DOM
        ele = $(ele).fadeTo('normal', .5).clone();
        bind_remove(
            $(ele)
                .data('pk', pk)
                .appendTo(target)
                .hide()
                .css('cursor', '')
                .slideDown('normal')
        );
    };

    var remove_object = function(ele){
        // remove it from the field
        var pk = $(ele).data('pk');
        var vals = $(hidden).val().split(',');
        var str = '';
        for(var i = 0; i < vals.length; i++){
            if(vals[i] && pk != vals[i]){
                str += vals[i] + ',';
            }
        }
        $(hidden).val(str);

        // remove the element
        $(ele).slideUp('normal', function(){
            $(this).remove();
        })

        // unfade it in the choices area
        $(p + '_wrapper .ajax_search .results > span').each(function(){
            if(pk == $(this).data('pk')){
                $(this)
                    .fadeTo('normal', 1)
                    .css('cursor', 'pointer')
                    .one('click', function(){add_object(this);})
                    .hover(function(){
                        $(this).css('background-color', '#eeeeee');
                    }, function(){
                        $(this).css('background-color', '');
                    });
            }
        });
    };

    // returns true if the content has already been selected
    var already_added = function(pk){
        var arr = $(hidden).val().split(',')
        for(var i = 0; i < arr.length; i++){
            if(arr[i] && arr[i] == pk) return true;
        }
        return false;
    };

    // processes the ajax response
    //   dump each object into the results area, bind click handlers, etc
    var process_response = function(url_base, data){
        // dump results into .results and bind click handlers
        var target = $(p + '_wrapper .ajax_search .results');
        $(target).empty();
        if(data.objs.hasOwnProperty('empty')){
            $(target).append('<span>No content found.</span>');
        } else {
            $.each(data.objs, function(pk, html){
                var ele = $(html);
                $(ele)
                    .appendTo(target)
                    .data('pk', pk)
                    .one('click', function(){add_object(this);})
                    .css('cursor', 'pointer')
                    .hover(function(){
                        $(this).css('background-color', '#eeeeee');
                    }, function(){
                        $(this).css('background-color', '');
                    });
                if(already_added(pk)){
                    $(ele)
                        .css('cursor', '')
                        .unbind()
                        .fadeTo('normal', .5);
                }
            });
        }
        // create paging links
        var p_link = (data.prev_page == 0) ? '' : '<a href="#">Prev</a>';
        var n_link = (data.next_page == 0) ? '' : '<a href="#">Next</a>';
        target = $(p + '_wrapper .ajax_search .paging_links');
        $(target).empty();
        if(p_link){
            $(p_link)
                .appendTo(target)
                .click(function(){
                    $.getJSON(url_base + '&page=' + data.prev_page, function(data){
                        process_response(url_base, data);
                    })
                    return false;
                });
        }
        $(target).append('&nbsp;');
        if(n_link){
            $(n_link)
                .appendTo(target)
                .click(function(){
                    $.getJSON(url_base + '&page=' + data.next_page + '/', function(data){
                        process_response(url_base, data);
                    })
                    return false;
                });
        }
    };

    $(p + '_wrapper div.chosen_objs').sortable({stop: function(){
        // reset value of hidden on sort
        $(hidden).val('');
        $(p + '_wrapper div.chosen_objs > span').each(function(){
            $(hidden).val($(hidden).val() + $(this).data('pk') + ',');
        });
    }});

    var ids = $(hidden).val().split(',');
    $(p + '_wrapper div.chosen_objs > span').each(function(i){
        $(this).data('pk', ids[i]);
        bind_remove(this);
    });

    // send ajax search request
    $(p + '_go').click(function(){
        var args = {};
        args.tags = $(p + '_tags').val();
        args.start_d = $(p + '_start_date').val();
        args.end_d = $(p + '_end_date').val();
        $.getJSON(ajax_url, args, function(data){
            process_response(args, data);
        });
        return false;
    });
};
