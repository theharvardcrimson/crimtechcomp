/*!
 * @overview adblock-blocker
 *     Attempt to detect if a user on the is running an
 *     adblocker when trying to access The Crimson Online.
 *     If they are, display a closeable popup requesting that
 *     they turn it off and display a banner ad replacement message.
 * @author Alex Wendland (me@alexwendland.com)
 * @author Nenya Edjah (nenya.edjah@thecrimson.com)
 */

$(document).ready(function() {
    /* How many times a day should the closeable popup show up? */
    var adblock_popup_frequency = 1;

    /* How many milliseconds should the user wait to see the continue button? */
    var continue_button_appear_delay = 0;

    /* After how many pages should the popup appear? 0 is immediately on the first visit */
    var popup_page_count_delay = 1;

    /* How many milliseconds will the popup be delayed from appearing after opening a page? */
    var popup_appear_delay = 15000;


    /* Sets a cookie to a specific value. Expire it after 1/freq of a day */
    function setCookie(name, val, freq) {
        var d = new Date();
        d.setTime(d.getTime() + 24 * 60 * 60 * 1000 / freq);
        document.cookie = name + '=' + val + '; expires=' + d.toUTCString() + '; path=/';
    }

    /* Obtains the value of a cookie */
    function getCookieValue(name) {
        var c = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return c ? c.pop() : '';
    }

    /* Deletes a cookie */
    function deleteCookie(name) {
        var d = new Date();
        d.setTime(d.getTime() - 1873);
        document.cookie = name + '=; expires=' + d.toUTCString() + '; path=/';
    }

    /* Create DOM elements */
    function createDom(html) {
        var fragment = document.createElement('div');
        fragment.innerHTML = html;
        return fragment.children;
    }

    /**********************
     * Ad-block detection *
     **********************/

    /**
    * Determines if the user should be shown the anti-adblock popup.
    * They will still be shown the anti-adblock banner.
    */
    function shouldShowPopup() {
        if (getCookieValue('adblock_popup'))
            return false;

        var pageCount = +getCookieValue('popup_page_count');
        if (pageCount >= popup_page_count_delay) {
            setCookie('adblock_popup', 'inactive', adblock_popup_frequency);
            deleteCookie('popup_page_count');
            return true;
        } else {
            setCookie('popup_page_count', pageCount + 1, 144);
            return false;
        }
    }


    var crimsonLogo = 'https://s3.amazonaws.com/static.thecrimson.com/images/logo.svg';
    var regularBannerImg = 'https://s3.amazonaws.com/static.thecrimson.com/images/727x89-adblock-banner.svg';
    var mobileBannerImg = 'https://s3.amazonaws.com/static.thecrimson.com/images/355x110-adblock-banner.svg';
    /**
    * This is a nonintrusive method. It shows an anti-adblock
    * message in place of the main banner ad
    */
    function showBannerMessage() {
        var regularBannerMessage = createDom(
            '<div class="leaderboardclone">' +
                '<div class="adblock-banner">' +
                    '<img src="'+ regularBannerImg + '" width="728px" height="90px">' +
                '</div>' +
            '</div>')[0];
        var mobileBannerMessage = createDom(
            '<div class="adblock-banner">' +
                '<img src="'+ mobileBannerImg + '" width="320px" height="100px">' +
            '</div>')[0];
        var mobileBanner = document.getElementsByClassName('mobile-banner')[0];
        while (mobileBanner.firstChild)
            mobileBanner.removeChild(mobileBanner.firstChild);
        mobileBanner.appendChild(mobileBannerMessage);

        var content = document.getElementById("content");
        content.insertBefore(regularBannerMessage, content.firstChild);
    }


    /**
    * This pop up will only appear once in a while.
    * It can be closed by clicking continue.
    */
    function showCloseablePopup() {
        showBannerMessage();
        if (shouldShowPopup()) {
            setTimeout(function() {
                ga('send', 'event', 'adblock', 'popup_appear');
                var blockedAlertElem = createDom('' +
                    '<div class="adblock">' +
                        '<div class="adblock__content">' +
                            '<div class="adblock__image">' +
                                '<img style="max-width: 70px" src="' + crimsonLogo + '">' +
                            '</div>' +
                            '<div class="adblock__message">' +
                                'The Harvard Crimson is an entirely student-run nonprofit that relies on advertising revenue. ' +
                                'Please support us by disabling AdBlock for our site. Thank you.' +
                            '</div>' +
                            '<div class="adblock__links">' +
                                '<div class="adblock__helplink">' +
                                    '<a class="adblock__link" href="http://www.wikihow.com/Disable-Adblock" target="_blank"><em>Need help with this?</em></a>' +
                                '</div>' +
                                '<div class="adblock__ignore">' +
                                    '<a class="adblock__link" href="javascript:void(0)"><em>Show me The Crimson anyway &gt;</em> </a>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>')[0];
                var body = document.getElementsByTagName('body')[0];
                body.appendChild(blockedAlertElem);
                body.classList.add('adblocker-enabled');

                var button = document.getElementsByClassName('adblock__ignore')[0];
                button.style.visibility = 'hidden';
                button.addEventListener('click', function() {
                    body.removeChild(blockedAlertElem);
                    body.classList.remove('adblocker-enabled');
                });

                var help = document.getElementsByClassName('adblock__helplink')[0];
                help.addEventListener('click', function() {
                    ga('send', 'event', 'adblock', 'helplink_clicked');
                });

                setTimeout(function() {
                    button.disabled = false;
                    button.style.visibility = 'visible';
                }, continue_button_appear_delay);
            }, popup_appear_delay);
        }
    }


    /**
    * Determines whether or not AdBlock is enabled and takes actions depending
    * on the result
    */
    function runAdBlockHandler(adBlockMessaging) {
        $.ajax({
            url: "https://s3.amazonaws.com/static.thecrimson.com/js/ads.js",
            success: function() {
                if (getCookieValue('has_adblock')) {
                    // Send info to Google analytics that a user has disabled adblock
                    deleteCookie('has_adblock');
                    ga('send', 'event', 'adblock', 'disable');
                }
            },
            error: function() {
                // Display anti-adblock measures
                adBlockMessaging();
                setCookie('has_adblock', 'true', 1);
            }
        });
    }

    !mobileAndTabletcheck() && runAdBlockHandler(showCloseablePopup);

});
