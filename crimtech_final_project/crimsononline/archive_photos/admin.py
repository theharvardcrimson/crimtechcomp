import logging

from .models import ArchiveImage

from crimsononline.common.forms import ContributorChoicesAddField, JSTreeWidget
from crimsononline.content.admin import ContentAdmin, ContentModelForm

logger = logging.getLogger(__name__)


class ArchiveForm(ContentModelForm):
    contributors = ContributorChoicesAddField()

    class Meta:
        model = ArchiveImage
        fields = '__all__'
        # NOTE: hidden inlcude, section, width, height
        widgets = {
            'archive_category': JSTreeWidget,
        }


class ArchiveImageAdmin(ContentAdmin):
    list_display = ('title', 'admin_thumb', 'pk',)
    list_display_links = ('admin_thumb', 'title',)
    list_per_page = 80
    list_filter = ('mark_important', 'archive_category')
    search_fields = ('title', 'description',)

    form = ArchiveForm
    fields = ('title', 'subtitle', 'section', 'subject', 'contributors', 'pic',
              'crimson_owned', 'issue', 'year', 'month', 'day', 'description',
              'location', 'show_online', 'sell_online', 'mark_important',
              'archive_category', 'tags', 'slug', 'needs_attention', 'notes',
              'pub_status', 'group', 'delete_group')

    class Media:
        js = (
            'scripts/jquery.js',
            'scripts/admin/Article.js',
            'scripts/admin/framework/jquery.sprintf.js',
            'scripts/noenter.js',
        )
