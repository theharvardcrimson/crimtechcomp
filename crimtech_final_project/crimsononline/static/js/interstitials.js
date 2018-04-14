var Crimson = Crimson || {};

/*
    Related files:
      - base.css hides relevant divs
      - __base.html defines relevant divs
*/

Crimson.Interstitials = (function($) {
    var COOKIE_NAME = 'crimson.interstitials';
    var COOKIE_OPTIONS = { expires: 20 * 365, path: '/' };
    var COOKIE_VERSION = 2;

    var MODAL_SELECTOR = '#modal';
    var CONTENT_SELECTOR = '#interstitial';

    var disabled = false;

    var interstitials = {};
    var $modal;
    var $content;

    var active_interstitial;
    var checkCambridge = false;

    var create = function(name, options) {
        var defaults = {
            url: '', // URL for the interstitial code
            excludeUrls: [], // URLs where the interstitial won't be DISPLAYED. These URLs still count for Page Views
            interval: 0.5, // Number of days between interstitial showings
            pv_delay: 0, // Number of Page Views before displaying this particular interstitial
                         // i.e. 2 means the second PV, 0 means none
            pv_elapsed: 1, // Number of Page Views elapsed in session % pv_delay
            delay: 0, // Time delay (in ms) between page load and intersitial display
            autorun: true, // Puts interstitial in queue to be automatically displayed
            lastShown: new Date(0), // Last time this interstitial was displayed
            show_immediately: true, // Set interstitial to both fill and display when activated
            passed: false, // Internal variable to mark that an interstitial was unmarked
            check_outside_cambridge: false,
            outside_cambridge_pv_delay: 0
        };
        options = $.extend(defaults, options);
       // alert("ass"+options.interval+options.url);


        if (options.check_outside_cambridge)
            checkCambridge = true;

        options.pv_elapsed = options.pv_elapsed % options.pv_delay;

        if (name === '')
            throw new Error('Crimson.Interstitial.create(): ' +
                'must provide unique name for interstitial');
        if (name in interstitials)
            throw new Error('Crimson.Interstitial.create(): ' +
                'interstitial with this name already exists');
        if (options.url === '')
            throw new Error('Crimson.Interstitial.create(): ' +
                'must specify url for interstitial');

        interstitials[name] = options;
        return options;
    };

    var display = function() {
        $(document.body).addClass('modal-open');
        $modal.fadeIn(400);
        setTimeout(function() {
            $content.slideDown(300);
        }, 265);
        _registerEvent(active_interstitial);
    };

    var show = function(name) {
        _fill(name, true);
    };

    var hide = function(e) {
        $content.slideUp(300);
        setTimeout(function() {
            $modal.fadeOut(400);
        }, 200);
        $(document.body).removeClass('modal-open');
        Crimson.Interstitials.onHide();
        if (typeof e !== 'undefined')
            e.preventDefault();
    };

    var reset = function() {
        $.removeCookie(COOKIE_NAME, COOKIE_OPTIONS);
    };

    var unmark = function(name) {
        // Note that an interstitial was not in fact shown
        // even though it was found and shown.
        interstitials[name].lastShown = new Date(0);
        interstitials[name].pv_elapsed = -1; // Make it try again next page
        interstitials[name].passed = true;
        _writeCookie();
        _findAndShow(); // search for another interstitial
    };

    var _fill = function(name, display_after) {
        active_interstitial = name;
        display_after = typeof display_after !== 'undefined' ? display_after : true;
        if ($(window).width() > 640 || name !== "subscribe") {
            interstitials[name].lastShown = new Date();
            $content.load(interstitials[name].url, function() {
                if (display_after) {
                    display();
                }
            });
            _writeCookie();
        }
    };

    var _loadElements = function() {
        $modal = $(MODAL_SELECTOR);
        $content = $(CONTENT_SELECTOR);
    };

    var _writeCookie = function() {
        var data = {
            version: COOKIE_VERSION,
            disabled: disabled,
            lastVisited: Date.now(),
            interstitials: {}
        };
        $.each(interstitials, function(name, options) {
            data.interstitials[name] = {};
            data.interstitials[name].lastShown = options.lastShown.getTime();
            data.interstitials[name].pv_elapsed = ((options.pv_elapsed+1) % options.pv_delay);
        });
        $.cookie(COOKIE_NAME, data, COOKIE_OPTIONS);
    };

    var _readCookie = function() {
        var cookie = $.cookie(COOKIE_NAME);
        if (cookie && cookie.version && cookie.version == COOKIE_VERSION) {
            if (cookie.disabled)
                disabled = true;

            lastVisited = new Date(cookie.lastVisited);
            keep_cookie_pv = lastVisited.getDate() == (new Date()).getDate();

            $.each(cookie.interstitials, function(name, obj) {
                try {
                    interstitials[name].lastShown = new Date(obj.lastShown);
                    if (keep_cookie_pv)
                        interstitials[name].pv_elapsed = obj.pv_elapsed;
                }
                catch (TypeError) {}
            });
        }
    };

    var _listenForClose = function() {
        $content.on('click', '.interstitial-close', hide);
        $modal.on('click', hide);
        $content.on('click', function(e) { e.stopPropagation(); });
    };

    // register google analytics event for showing interstitial
    var _registerEvent = function(name) {
        var category = 'interstitial';
        var action = 'show';
        var label = name; // subscribe, ad, etc.
        var non_interaction = true; // don't include interstitial event in bounce rate calculation
        ga('send', 'event', category, action, label, {'nonInteraction': non_interaction});
    };

    var _findAndShow = function () {
        $.each(interstitials, function(name, options) {
            if ($.inArray(window.location.pathname, options.excludeUrls) == -1) {
                var time_elapsed = Date.now() - options.lastShown;
                //alert(time_elapsed+"," +1000 * 60 * 60 * 24 * options.interval + ","+ options.autorun,+","+options.pv_elapsed);
              //  if (!options.passed && options.pv_elapsed === 0 && time_elapsed > 1000 * 60 * 60 * 24 * options.interval && options.autorun) {//
                if ( time_elapsed > 1000 * 60 * 60 * 24 * options.interval && options.autorun) {
                     //alert("Interstitial");
                    setTimeout(function() { _fill(name, options.show_immediately); }, options.delay);
                    return false; // Makes it so one PV only has one interstitial!
                                  //   Only the first interstitial is put in queue, the rest are ignored
                                  //   and will be shown after the next PV cycle -- assuming this interstitial
                                  //   is shown so next time this code won't be reached for that interstitial
                }
            }
        });

        return; // if too few page views have occurred to display interstitial, don't display any
    };

    var onHide = function() {};

    var _geoCheckThenComplete = function() {
        $.get('http://www.thecrimson.com/ajax/is_local/',
                function(data, status) {
                    if (data === 'False') {
                        $.each(interstitials, function(name, options) {
                            if (options.check_outside_cambridge)
                                options.pv_delay = options.outside_cambridge_pv_delay;

                            options.pv_elapsed = options.pv_elapsed % options.pv_delay;

                            interstitials[name] = options;
                        });
                    }
                    // else => data == 'True' || data == 'Unknown'

                     _completeLoading();
                });
    };

    $(document).ready(function() {
        if (checkCambridge)
            _geoCheckThenComplete();
        else
            _completeLoading();
    });

    var _completeLoading = function() {
        $.cookie.json = true;
        _loadElements();
        _readCookie();
        if (!disabled) {
            _findAndShow();
            _writeCookie();
            _listenForClose();
        }
    };

    return {
        reset: reset,
        create: create,
        show: show,
        hide: hide,
        onHide: onHide,
        display: display,
        unmark: unmark
    };
}(jQuery));
