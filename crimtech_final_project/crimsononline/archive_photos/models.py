import itertools

from django.db import models

from crimsononline.content.models import Image, ImageManager


class ArchiveImage(Image):
    crimson_owned = models.IntegerField(
        choices=((1, 'Yes'), (0, 'No'), (2, 'Unsure')))
    location = models.CharField(max_length=100, default='', blank=True)
    subject = models.CharField(max_length=100, default='', blank=True)
    show_online = models.BooleanField(default=True)
    sell_online = models.BooleanField(default=False)
    mark_important = models.BooleanField(default=False)
    notes = models.TextField(default='', blank=True)
    archive_category = models.ForeignKey('ArchiveCategory', null=False)
    needs_attention = models.BooleanField(default=False)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)

    objects = ImageManager()

    def save(self, *args, **kwargs):
        self.is_archiveimage = True
        return super(ArchiveImage, self).save(*args, **kwargs)


class ArchiveCategory(models.Model):
    parent = models.ForeignKey('ArchiveCategory',
                               null=True, related_name='children')
    name = models.CharField(max_length=100, default='')

    def content(self):
        content_sets = []
        cats = [self]
        while len(cats) > 0:
            cat = cats.pop()
            content_sets.append(ArchiveImage.objects.filter(category=cat))
            cat.extend(cat.children)

        return list(itertools.chain(*content_sets))

    def get_level(self):
        if self.parent is None:
            return 0
        else:
            return self.parent.get_level() + 1

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('parent', 'name')
