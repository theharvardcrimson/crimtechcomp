import json
import logging
import urllib
from datetime import datetime, timedelta

from crimsononline.common.utils.date import to_js_timestamp

logger = logging.getLogger(__name__)


class NewsletterSubscribeMiddleware(object):
    def process_response(self, request, response):
        """
        Hides the newlsetter interstitial if the link came
        from a newsletter.
        """
        src = request.GET.get('utm_source', None)
        if src == 'Email Newsletter':
            self.record_newsletter_interaction(request, response)
        return response

    @staticmethod
    def record_newsletter_interaction(request, response):
        """
        Updates the subscribe cookie so that it won't be shown
        for another month. This function is used by the middleware
        function above and by the tracking pixel defined in
        view.py:subscribe_track.
        """
        try:
            plus_one_month = datetime.today() + timedelta(weeks=4)
            timestamp = to_js_timestamp(plus_one_month)

            cookie = request.COOKIES['crimson.interstitials']
            data = json.loads(urllib.unquote(cookie))
            data['interstitials']['subscribe']['lastShown'] = timestamp

            cookie = urllib.quote(json.dumps(data))
            response.set_cookie('crimson.interstitials', cookie, path='/')
        except:
            pass  # malformed cookie; catch 'em next time
