var set_issue_picker = function(hidden_input, spec_url){
    // grab the wrapper div and use only its children to avoid conflicts with other issue pickers
    var $this = $("#" + hidden_input + "-wrapper"),
        $daily = $this.find(".daily"),
        $special = $this.find(".special"),
        $hidden_input = $this.find("#" + hidden_input),
        $date_elem = $this.find("#" + hidden_input + "-input");

    // turns a date obj into a str of the calendar's format
    var make_datestring = function(date){
        var date_str = (date.getMonth() > 8 ) ? "" : "0";
        date_str += (date.getMonth() + 1) + "/";
        date_str += (date.getDate() > 9) ? "" : "0";
        date_str += date.getDate() + "/" + date.getFullYear();
        return date_str;
    };

    // show / hide different daily / special issue pickers
    $this.find(".meta input").click(function(){
        if($(this).val() == 'daily'){
            $daily.show();
            $special.hide();
            $hidden_input.val(
                make_datestring($date_elem.datepicker('getDate')));
        } else {
            $daily.hide();
            $special.show().trigger("change");
        }
    });

    // grab list of special issue from server
    $this.find(".special input").change(function(){
        if($(this).val().length == 4){
            var full_url = spec_url + "?year=" + $(this).val();
            $this.find(".special select").load(full_url);
        }
    }).keypress(function(e){
        // prevent enter from submitting the form
        if(e.which == 13){
            $(this).change().blur();
            return false;
        }
    });

    $this.find(".special select").change(function() {
        $hidden_input.val($(this).val());
    });

    $date_elem.datepicker({
        showStatus: true,
        showOn: "both",
        buttonImage: static_url + "admin/img/icon_calendar.gif",
        buttonImageOnly: true,
        mandatory: true,
        onSelect: function(dateText){
            $hidden_input.val(dateText);
        }
    });
};
