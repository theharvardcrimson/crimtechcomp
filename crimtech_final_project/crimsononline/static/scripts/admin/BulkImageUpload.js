// DO NOT MODEL YOUR CODE ON ANYTHING IN THIS FILE

$(function(){
    // Elements
    var $image_list = $("#items-form-container"),
        image_list = [];

    // Convert list of contributors to a format Select2 expects
    select2_contributors = Crimson.contributor_list.map(function(contributor) {
        return {
            id: contributor.pk,
            text: contributor.fields.first_name + " "
                + contributor.fields.middle_name + " "
                + contributor.fields.last_name + " "
        };
    });
    select2_tags = Crimson.tag_list.map(function(tag) {
        return {
            id: tag.pk,
            text: tag.fields.text
        };
    });

    // Initialize all existing images
    init_existing_rows($image_list.children());

    $('#drop-button').click(function(){
        // Simulate a click on the file input button to show the file browser dialog
        $(this).parent().find('input').click();
    });

    // Initialize the jQuery File Upload plugin
    $('#upload').fileupload({

        // This element will accept file drag/drop uploading
        dropZone: $('#drop'),

        // This is the url to upload images to
        url: "/imageuploadtarget",

        // This function is called when a file is added to the queue;
        // either via the browse button, or via drag/drop:
        add: function (e, data) {
            var jqXHR,
                new_row;

            console.log(e);
            console.log(data);
            image_list = image_list.concat(data.files);
            // Assume only one file for now
            new_row = append_image_form(data.files[0]);

            // Initialize Select2 widgets
            init_select2(new_row, select2_contributors, select2_tags);

            // Upload the file now that it's on the queue
            // Use the timeout to prioritize UI update
            setTimeout(function(){
                jqXHR = data.submit();
            }, 200);
        },

        progress: function(e, data){
            console.log(e);
            console.log(data);
        },

        fail: function(e, data){
            console.log(e);
            console.log(data);
        }

    });

    // Prevent the default action when a file is dropped on the window
    $(document).on('drop dragover', function (e) {
        e.preventDefault();
    });

    // "Render" the form template using the new form id
    function append_image_form(file) {
        var count = $image_list.children().length,
            template = $('#item-template').html(),
            compiled_form = template.replace(/__prefix__/g, count),
            $form_node;

        // Append the newly created form
        $image_list.prepend(compiled_form);
        $form_node = $('#item-' + count);

        // Track the file name
        if (file && file.name) {
            $form_node.find(".filename").val(file.name);
        }

        // Bind events
        bind_admin_box($form_node);
        bind_advanced_box($form_node);

        // Display a preview of the image
        read_preview($form_node, file);

        // Update form count
        $('#id_form-TOTAL_FORMS').attr('value', count + 1);

        return $form_node
    }

    /**
     * Loops over existing images (i.e. not added dynamically), and intializes
     * all important information. E.g. binds "admin" and "advanced" checkboxes,
     * initializes select2
     */
    function init_existing_rows($forms) {
        $forms.each(function(i, form) {
            var $form_node = $(form);
            bind_admin_box($form_node);
            bind_advanced_box($form_node);
            init_select2($form_node, select2_contributors, select2_tags);
        });
    }

    /**
     * Binds a checkbox so that it toggles the visibility of the specified field
     */
    function bind_generic_checkbox(form, checkbox_selector, toggled_field_selector) {
        var $target_checkbox = $(checkbox_selector, form),
            handler = function(e) {
                var $hidden_field = $(toggled_field_selector, form);

                // Unhide if checked, hide if unchecked
                if ($target_checkbox.is(':checked')) {
                    $hidden_field.removeClass('hidden-animate');
                } else {
                    $hidden_field.addClass('hidden-animate');
                }
            }

        // Bind 'onclick' listener
        $target_checkbox.click(handler);

        // Run handler once to update
        handler();
    }

    /**
     * Bind admin checkbox that toggles the visibility of admin fields
     */
    function bind_admin_box(form) {
        bind_generic_checkbox(
            form,
            'input.publishable' /*checkbox_selector*/,
            'div.fields-publishing' /*toggled_field_selector*/
        );
    }

    /**
     * Bind advanced checkbox that toggles the visibility of advanced fields
     */
    function bind_advanced_box(form) {
        bind_generic_checkbox(
            form,
            'input.advanced' /*checkbox_selector*/,
            'div.fields-advanced' /*toggled_field_selector*/
        );
    }

    /**
     * Load the image from disk and preview it
     */
    function read_preview($row, file) {
        // Quick check
        if (!file) {
            return;
        }

        // Select the image we're using
        var $img = $('.image-placeholder img', $row),
            reader = new FileReader();

        // When the reader has read the file, fill the img's source
        reader.onload = function (event) {
            $img.attr('src',event.target.result);
        }
        reader.readAsDataURL(file);
    }

    /**
     * Initializes Select2 widget with shared data. TODO: Refactor
     */
    function init_select2($row, contributors, tags) {
        $row.find(".contributors").select2({
            data: contributors,
            multiple: true,
            minimumInputLength: 2
        });
        $row.find(".tags").select2({
            data: tags,
            multiple: true,
            minimumInputLength: 2
        });
    }
});
