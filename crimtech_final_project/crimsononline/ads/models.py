from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from sortedm2m.fields import SortedManyToManyField


class AdUnitManager(models.Manager):
    def create_or_update(self, **kwargs):
        if 'network_id' not in kwargs:
            raise ValueError('must specify network_id keyword argument')
        try:
            pk = self.get(network_id=kwargs['network_id']).pk
        except ObjectDoesNotExist:
            pk = None
        self.model(pk=pk, **kwargs).save()


class AdUnit(models.Model):
    # DEFUNCT 2015-02-07
    # MOBILE/DESKTOP distinctions no longer made. Requires database
    # migration before we can delete non-commented code.
    MOBILE_AND_DESKTOP = 0
    MOBILE_ONLY = 1
    DESKTOP_ONLY = 2
    DISPLAY_CHOICES = (
        (MOBILE_AND_DESKTOP, 'BOTH'),
        (MOBILE_ONLY, 'Mobile'),
        (DESKTOP_ONLY, 'Desktop'),
    )
    code = models.CharField(max_length=255, unique=True)
    network_id = models.CharField(max_length=100, unique=True)
    size = models.CharField(max_length=100)
    display_on = models.IntegerField(choices=DISPLAY_CHOICES,
                                     default=MOBILE_AND_DESKTOP)

    objects = AdUnitManager()

    class Meta:
        ordering = ['-size', 'code']

    def __unicode__(self):
        return self.code

    def dimensions(self):
        return [int(dim) for dim in self.size.split('x')]


class AdZoneManager(models.Manager):
    def units_for_placement(self, size, mobile, zone_name='default'):
        try:
            ad_zone = self.get(name=zone_name)
        except ObjectDoesNotExist:
            return []
        return ad_zone.ad_units.filter(size=size)


class AdZone(models.Model):
    name = models.CharField(max_length=255)
    ad_units = SortedManyToManyField(AdUnit)

    objects = AdZoneManager()

    def __unicode__(self):
        return self.name
