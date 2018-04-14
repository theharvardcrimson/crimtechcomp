var Crimson = Crimson || {};

// 600 x 500 interstitial ad
Crimson.Interstitials.create("ad_600x500", {
    url: '/interstitials/ad_600x500/',
    interval: 0.125,    // display eight times a day
    pv_delay: 1,    // display on first PV
    show_immediately: false
});

Crimson.Interstitials.create("subscribe", {
	url: '/subscribe/online/',
	excludeUrls: ['/', '/subscribe'],
    interval: 3, // display once every three days
	delay: 200
});

/* Crimson.Interstitials.create("store", {
	url: '/interstitial_store/',
	interval: 2,
	delay: 20,
}); */

$(function () {
    $("time").each(function() {
    	var date = moment($(this).attr("datetime")).max();
    	var now = moment();
    	if (now.diff(date, 'days') <= 4) {
    		$(this).text(date.fromNow());
    	}
    });
});
