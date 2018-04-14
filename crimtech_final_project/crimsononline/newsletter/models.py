import logging
from datetime import datetime
from os.path import splitext

from django.db import models

from premailer import Premailer

from crimsononline.common.utils.strings import rand_str

logger = logging.getLogger(__name__)

class Newsletter(models.Model):
    TYPE_CHOICES = (
        (0, 'Daily Newsletter'),
        (1, 'News Alert'),
        (2, 'Harvard Today'),
        (3, 'FM Newsletter'),
        (4, 'Sports Newsletter'),
        (5, 'Alumni Newsletter'),
        (7, 'Letterhead Message'),
        (8, 'Arts Newsletter'),
        (9, 'Parents Newsletter'),
        (10, 'Daily Briefing')
    )

    newsletter_type = models.IntegerField(default=0, choices=TYPE_CHOICES)
    layout_instance = models.ForeignKey(
        'placeholders.LayoutInstance', null=False)
    created_on = models.DateTimeField(null=False)
    send_date = models.DateField(db_index=True, blank=True, null=False)
    inline_css = models.BooleanField(default=True)
    ab_split = models.BooleanField(
        default=True, verbose_name='A/B split',
        help_text='Enable an A/B split test')
    subject = models.CharField(max_length=255, blank=True)
    text = models.TextField(default='', blank=True)

    class Meta:
        get_latest_by = 'send_date'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = datetime.today()
        if not self.send_date:
            self.send_date = datetime.today()
        return super(Newsletter, self).save(*args, **kwargs)

    def get_output(self):
        if self.inline_css:
            return self.get_inline_output()
        else:
            return self.get_raw_output()

    def get_inline_output(self):
        """
        Returns the inlined version of the email
        """

        p = Premailer(self.get_raw_output().decode('utf-8'),
                      exclude_pseudoclasses=True,
                      include_star_selectors=True,
                      remove_classes=False,
                      strip_important=False)
        return p.transform().replace('%7C', '|')

    def get_ad_for_position(self, pos_id):
        n = NewsletterAdFill.objects.filter(start_date__lte=self.send_date,
                                            end_date__gte=self.send_date,
                                            position=pos_id,
                                            newsletter_id=self.newsletter_type,
                                            enabled=True).order_by('-priority')
        if n:
            return n[0].ad_copy
        else:
            return None

    def get_default_layout(self):
        if self.newsletter_type == 0:
            return 'Daily Newsletter Template'
        elif self.newsletter_type == 1:
            return 'Newsletter Alert Template'
        elif self.newsletter_type == 3:
            return 'FM Newsletter Template'
        elif self.newsletter_type == 6:
            return 'Special Report Newsletter Template'
        elif self.newsletter_type == 10:
            return 'Daily Briefing Template'
        else:
            return 'Daily Newsletter Template'

    def get_raw_output(self):
        """
        Returns the rendered LayoutInstance, regardless of whether
        inlining is required
        """
        return self.layout_instance.render_to_string({
            'newsletter_obj': self, 'newsletter_name':
            self.TYPE_CHOICES[self.newsletter_type][1]})

    def __unicode__(self):
        choices = dict(self.TYPE_CHOICES)
        return '{0} - {1}'.format(
            choices[self.newsletter_type], self.send_date)


class HarvardTodayNewsletter(Newsletter):
    photo_description = models.TextField(default='', blank=True)
    weather_description = models.TextField(default='', blank=True)
    lunch_description = models.TextField(default='', blank=True)
    dinner_description = models.TextField(default='', blank=True)
    article_list = models.TextField(default='', blank=True)
    others_list = models.TextField(default='', blank=True)

    # Others includes Video of the day and random stuff.

    class Meta:
        get_latest_by = 'send_date'

    def get_default_layout(self):
        return 'Harvard Today Newsletter Template'

    def get_raw_output(self):
        """
        Returns the rendered LayoutInstance, regardless of whether
        inlining is required
        """
        return self.layout_instance.render_to_string({'newsletter_obj': self})

    def save(self, *args, **kwargs):
        self.newsletter_type = 2  # harvard today newsletter
        super(HarvardTodayNewsletter, self).save(*args, **kwargs)

    def __unicode__(self):
        return 'Harvard Today - {0}'.format(self.send_date)


class HarvardTodayEvent(models.Model):
    time = models.CharField(max_length=20, default='')
    description = models.TextField(default='')
    newsletter = models.ForeignKey(
        'HarvardTodayNewsletter', null=False, related_name='events')


class HarvardTodaySponsoredEvent(models.Model):
    time = models.CharField(max_length=20, default='')
    description = models.TextField(default='')
    newsletter = models.ForeignKey(
        'HarvardTodayNewsletter', null=False, related_name='sponsored_events')


def newsletter_image_get_save_path(instance, filename):
    ext = splitext(filename)[1]
    key = rand_str(10) if instance.pk is None else str(instance.pk)
    return datetime.now().strftime('newsletter/%Y/%m/%d/%H%M%S_') + key + ext


class NewsletterAd(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    pic = models.ImageField(
        upload_to=newsletter_image_get_save_path, null=False)
    link = models.CharField(max_length=150, blank=True, null=False)

    def save(self, *args, **kwargs):
        self.link = self.link.strip()
        if self.link[:7] != 'http://' and self.link[:8] != 'https://':
            self.link = '%s%s' % ('http://', self.link)
        super(NewsletterAd, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class NewsletterAdFill(models.Model):
    POSITION_CHOICES = (
        (0, 'Top'),
        (1, 'Bottom'),
    )
    ad_copy = models.ForeignKey(NewsletterAd, null=False)
    enabled = models.BooleanField(default=True)
    newsletter_id = models.IntegerField(
        default=0, choices=Newsletter.TYPE_CHOICES,
        verbose_name='Newsletter Type')
    position = models.IntegerField(default=0, choices=POSITION_CHOICES)
    start_date = models.DateField(db_index=True, null=False)
    end_date = models.DateField(db_index=True, null=False)
    priority = models.IntegerField(
        default=1,
        help_text='If multiple ads are scheduled for the same newsletter and '
                  'date, the one with the higher priority is chosen.')
