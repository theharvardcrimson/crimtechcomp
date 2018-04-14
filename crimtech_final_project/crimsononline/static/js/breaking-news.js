var Crimson = Crimson || {};

Crimson.BreakingNews = (function ($) {
	var COOKIE_NAME = 'crimson.breaking-news';
	var COOKIE_OPTIONS = { expires: 20 * 365, path: '/' };
	var BAR_SELECTOR = '#breaking-news';
	var DISMISS_SELECTOR = '#breaking-news-dismiss';

	var timestamp;
	var $bar;
	var $dismiss;

	$(document).ready(function() {
		$bar = $(BAR_SELECTOR);
		$dismiss = $(DISMISS_SELECTOR);
		timestamp = $dismiss.attr('data-timestamp');

		if ($.cookie(COOKIE_NAME) != timestamp) {
			$bar.show();
		}

		$dismiss.click(function(e) {
			e.preventDefault();
			$.cookie(COOKIE_NAME, timestamp, COOKIE_OPTIONS);
			$bar.slideUp();
		});
	});

	return { }
})(jQuery);
