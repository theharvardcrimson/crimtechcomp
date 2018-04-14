$(document).ready(function() {
    $(".jstree").jstree({
        "core": {
            "themes": {
                "icons": false
            }
        }
    });

    $('.jstree').on('changed.jstree', function (e, data) {
        $(this).siblings('input').first().val(data.selected);
    });
});
