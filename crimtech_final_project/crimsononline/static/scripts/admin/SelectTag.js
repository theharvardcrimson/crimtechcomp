/*
SelectTag2 - Turns a multiple-select box into a filter interface.

Different than SelectTag because this is coupled to the admin framework.

Requires core.js, SelectBox.js and addevent.js.
*/

function findForm(node) {
    // returns the node of the form containing the given node
    if (node.tagName.toLowerCase() != 'form') {
        return findForm(node.parentNode);
    }
    return node;
}

var SelectTag = {

    addOption: function(id,tag,redisplay) {
        // $("#id_tags_from").append("<option value='" + id + "'>" + tag + "</option>");
        option = new Object();
        option.value = id;
        option.text = tag;
        SelectBox.add_to_cache("id_tags_from",option);
        if(redisplay){
            SelectBox.redisplay("id_tags_from");
        }
    },

    clearSelect: function() {
        SelectBox.cache["id_tags_from"] = new Array();
        // $("#id_tags_from").empty();
        SelectBox.redisplay("id_tags_from");
    },

    move: function (from, to) {

        var from_box = document.getElementById(from);
        var to_box = document.getElementById(to);
        var option;
        for (var i = 0; (option = from_box.options[i]); i++) {
            if (option.selected && SelectBox.cache_contains(from, option.value)) {

                SelectBox.add_to_cache(to, {value: option.value, text: option.text, displayed: 1});
                SelectBox.delete_from_cache(from, option.value);

                // Adding a tag
                if(from == "id_tags_from") {
                    for (var category in tag_list) {
                        for (var value in tag_list[category]) {
                            if (tag_list[category][value] == option.text) {
                                tags_in_use[category][value] = tag_list[category][value];
                                delete tag_list[category][value];
                            }
                        }
                    }
                }

                // Removing a tag
                if(from == "id_tags_to") {
                    for (var category in tags_in_use) {
                        for (var value in tags_in_use[category]) {
                            if (tags_in_use[category][value] == option.text) {
                                tag_list[category][value] = tags_in_use[category][value];
                                delete tags_in_use[category][value];
                            }
                        }
                    }
                }
            }
        }
        SelectBox.redisplay(from);
        SelectBox.redisplay(to);
    },

    init: function(field_id, field_name, is_stacked, admin_media_prefix) {
        var from_box = document.getElementById(field_id);
        from_box.id += '_from'; // change its ID
        from_box.className = 'filtered';

        // Remove <p class="info">, because it just gets in the way.
        var ps = from_box.parentNode.getElementsByTagName('p');
        for (var i=0; i<ps.length; i++) {
            from_box.parentNode.removeChild(ps[i]);
        }

        // <div class="selector"> or <div class="selector stacked">
        var selector_div = quickElement('div', from_box.parentNode);
        selector_div.className = is_stacked ? 'selector stacked' : 'selector';

        // <div class="selector-available">
        var selector_available = quickElement('div', selector_div, '');
        selector_available.className = 'selector-available';
        quickElement('h2', selector_available, interpolate(gettext('Available %s'), [field_name]));
        var filter_p = quickElement('p', selector_available, '');
        filter_p.className = 'selector-filter';
        quickElement('img', filter_p, '', 'src', admin_media_prefix + 'img/selector-search.gif');
        filter_p.appendChild(document.createTextNode(' '));
        var filter_input = quickElement('input', filter_p, '', 'type', 'text');
        filter_input.id = field_id + '_input';
        selector_available.appendChild(from_box);
        var choose_all = quickElement('a', selector_available, gettext('Choose all'), 'href', 'javascript: (function(){ SelectTag.move_all("' + field_id + '_from", "' + field_id + '_to"); })()');
        choose_all.className = 'selector-chooseall';

        // <ul class="selector-chooser">
        var selector_chooser = quickElement('ul', selector_div, '');
        selector_chooser.className = 'selector-chooser';
        var add_link = quickElement('a', quickElement('li', selector_chooser, ''), gettext('Add'), 'href', 'javascript: (function(){ SelectTag.move("' + field_id + '_from","' + field_id + '_to");})()');
        add_link.className = 'selector-add';
        var remove_link = quickElement('a', quickElement('li', selector_chooser, ''), gettext('Remove'), 'href', 'javascript: (function(){ SelectTag.move("' + field_id + '_to","' + field_id + '_from");})()');
        remove_link.className = 'selector-remove';

        // <div class="selector-chosen">
        var selector_chosen = quickElement('div', selector_div, '');
        selector_chosen.className = 'selector-chosen';
        quickElement('h2', selector_chosen, interpolate(gettext('Chosen %s'), [field_name]));

        var to_box = quickElement('select', selector_chosen, '', 'id', field_id + '_to', 'multiple', 'multiple', 'size', from_box.size, 'name', from_box.getAttribute('name'));
        to_box.className = 'filtered';
        var clear_all = quickElement('a', selector_chosen, gettext('Clear all'), 'href', 'javascript: (function() { SelectTag.move_all("' + field_id + '_to", "' + field_id + '_from");})()');
        clear_all.className = 'selector-clearall';

        from_box.setAttribute('name', from_box.getAttribute('name') + '_old');

        // Set up the JavaScript event handlers for the select box filter interface
        addEvent(filter_input, 'keyup', function(e) { SelectTag.filter_key_up(e, field_id); });
        addEvent(filter_input, 'keydown', function(e) { SelectTag.filter_key_down(e, field_id); });
        addEvent(from_box, 'dblclick', function() { SelectTag.move(field_id + '_from', field_id + '_to'); });
        addEvent(to_box, 'dblclick', function() { SelectTag.move(field_id + '_to', field_id + '_from'); });
        addEvent(findForm(from_box), 'submit', function() { SelectBox.select_all(field_id + '_to'); });
        SelectBox.init(field_id + '_from');
        SelectBox.init(field_id + '_to');
        // Move selected from_box options to to_box
        SelectTag.move(field_id + '_from', field_id + '_to');
    },
    filter_key_up: function(event, field_id) {
        from = document.getElementById(field_id + '_from');
        // don't submit form if user pressed Enter
        if ((event.which && event.which == 13) || (event.keyCode && event.keyCode == 13)) {
            from.selectedIndex = 0;
            SelectTag.move(field_id + '_from', field_id + '_to');
            from.selectedIndex = 0;
            return false;
        }
        var temp = from.selectedIndex;
        SelectBox.filter(field_id + '_from', document.getElementById(field_id + '_input').value);
        from.selectedIndex = temp;
        return true;
    },
    filter_key_down: function(event, field_id) {
        from = document.getElementById(field_id + '_from');
        // right arrow -- move across
        if ((event.which && event.which == 39) || (event.keyCode && event.keyCode == 39)) {
            var old_index = from.selectedIndex;
            SelectTag.move(field_id + '_from', field_id + '_to');
            from.selectedIndex = (old_index == from.length) ? from.length - 1 : old_index;
            return false;
        }
        // down arrow -- wrap around
        if ((event.which && event.which == 40) || (event.keyCode && event.keyCode == 40)) {
            from.selectedIndex = (from.length == from.selectedIndex + 1) ? 0 : from.selectedIndex + 1;
        }
        // up arrow -- wrap around
        if ((event.which && event.which == 38) || (event.keyCode && event.keyCode == 38)) {
            from.selectedIndex = (from.selectedIndex == 0) ? from.length - 1 : from.selectedIndex - 1;
        }
        return true;
    }
}
