$(function() {
    var $window = $(window);
    var $body = $(document.body);
    var $start = $(".sticky-bar-start");
    $sidebar_start_scroll = 0;  // Window position when the sidebar was opened
    var $sidebar = $("#sidebar-menu");

    if ($start.length == 0) {
      return;
    }

    setInterval(function () {
        if ($window.scrollTop() < $start.offset().top + 20) {
            $body.addClass("first-screen");
            // Hide the sidebar when at the top of the page
            $sidebar.removeClass("sidebar-menu-visible");
        } else {
            $body.removeClass("first-screen");
        }

        // Hide the sidebar if the user scrolls more than 50px
        if (Math.abs($window.scrollTop() - $sidebar_start_scroll) > 50) {
            $sidebar.removeClass("sidebar-menu-visible");
        }
    }, 150);

    // Handle all sidebar-menu functionality
    $(".sidebar-menu-button").click(function() {
        $sidebar_start_scroll = $window.scrollTop();
        $("#sidebar-menu").toggleClass("sidebar-menu-visible");
    });

    $(document).mouseup(function(event) {
        // if the target of the click is not the $sidebar, and
        // not a descendant of the $sidebar, and not the
        // button being clicked
        if (!$sidebar.is(event.target)
            && $sidebar.has(event.target).length === 0
            && !$(".sidebar-menu-button").is(event.target))
        {
            $sidebar.removeClass("sidebar-menu-visible");
        }
    });
});
