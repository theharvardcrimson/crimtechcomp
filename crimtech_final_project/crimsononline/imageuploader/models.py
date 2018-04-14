from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

from crimsononline.content.models import Image, ImageManager


class BulkImage(Image):
    """
    Image uploads to be added to admin, uploaded to Smugmug, or archived
    """

    # Whether or not this goes into "Admin". Only for images ready to publish
    # TODO: move to content and make admin respect this
    publishable = models.BooleanField(default=False)
    # True => Upload to Smugmug
    sell_online = models.BooleanField(default=True)
    # Editor approval
    pending_review = models.BooleanField(default=True)

    objects = ImageManager()

    def save(self, *args, **kwargs):
        # Masquerade as a regular image for now
        # Fix content.models to handle deeper inheritance later
        self.content_type = ContentType.objects.get_for_model(Image)
        return super(BulkImage, self).save(*args, **kwargs)

    def get_admin_change_url(self):
        return reverse('admin:imageuploader_bulkimage_change', args=(self.pk,))
