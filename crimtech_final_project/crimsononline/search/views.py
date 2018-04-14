from django.conf import settings
from django.views.generic import TemplateView


class SearchView(TemplateView):
    template_name = 'search/index.html'

    def get_context_data(self):
        return {
            'custom_search_engine_id': settings.GOOGLE_CUSTOM_SEARCH_ENGINE_ID
        }
