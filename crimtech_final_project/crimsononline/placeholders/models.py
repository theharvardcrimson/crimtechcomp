import logging
import re

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, models
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render

import crimsononline.placeholders.templatetags.placeholders as placeholders
from crimsononline.content.models import Content

logger = logging.getLogger(__name__)


class PlaceholderList(list):
    title = None
    title_link = None
    extra_text = None


class Layout(models.Model):
    """
    Contains all of the information about a layout, and where to find its
    template, but is not associated to any placeholders.
    """

    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=300, blank=True)
    template_path = models.CharField(max_length=100, blank=False, unique=True)
    pic = models.ImageField(upload_to='layouts', blank=True, null=True)
    article_template = models.BooleanField(default=False)
    # XXX Fix this shit this sucks.
    # aww nikhil don't be so hard on yourself
    gallery_template = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class LayoutInstance(models.Model):
    """
    This is an individual layout object that actually gets associated to
    content (such as feature packages or sections). Note that template_path
    is not necessarily unique. This means that a single template could be
    associated with multiple different webpages.
    """

    name = models.CharField(max_length=50, blank=True)
    parent = models.ForeignKey(Layout, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    custom_html = models.TextField(blank=True)

    def __init__(self, *args, **kwargs):
        super(LayoutInstance, self).__init__(*args, **kwargs)
        try:
            self._initial_parent = self.parent
        except ObjectDoesNotExist:
            self._initial_parent = None

    def render(self, request=None, context=None):
        if not context:
            context = {}
        x = render(request,
                   self.parent.template_path,
                   self.augment_context(context))
        return x

    def render_to_string(self, context=None):
        if not context:
            context = {}
        x = render(HttpRequest(),
                   self.parent.template_path,
                   self.augment_context(context))
        return x.content

    def augment_context(self, context):
        """
        This (possibly) external method allows a view to use placeholders
        without using the above render method. Follow the model of
        Layout.render
        """
        if self not in context and 'crimsononline.layout' not in context:
            context['custom_html'] = self.custom_html
            context['crimsononline.layout'] = self
            context[self] = self.fill_placeholders()
        else:
            raise Exception('Invalid context: cannot use Layout object as '
                            'a key in context.')
        return context

    def fill_placeholders(self):
        """
        Generates a dictionary containing the actual content for all
        placeholders in the layout. This makes it so autofilling works
        in order. Not to be used externally in almost all cases.
        """
        context = dict()
        # note all manually placed content and get ready for autocontent
        placed = [c.pk
                  for placeholder in self.placeholders.order_by('position')
                  for c in placeholder.content]
        for placeholder in self.placeholders.order_by('position'):
            if placeholder.node:
                context[placeholder.name] = PlaceholderList()
                context[placeholder.name].title = placeholder.title
                context[placeholder.name].title_link = placeholder.title_link
                context[placeholder.name].extra_text = placeholder.extra_text

                autofiller = placeholder.get_autofiller() \
                                        .exclude(pk__in=placed)
                num_items = max(placeholder.min_items,
                                placeholder.content_relations.count(),
                                placeholder.autofill_number)

                auto_index = 0

                for i in range(num_items):
                    stored = placeholder.content_relations.filter(position=i)
                    if stored.count() == 1:
                        context[placeholder.name].append(
                            stored[0].content.child)
                    else:
                        # if requires media, skip ones without main_rel_content
                        if placeholder.require_media:
                            try:
                                has_media = autofiller[auto_index].child \
                                    .main_rel_content is not None
                            except AttributeError:
                                has_media = False
                            except IndexError:
                                break

                            while not has_media:
                                auto_index += 1
                                try:
                                    has_media = autofiller[auto_index].child \
                                        .main_rel_content is not None
                                except AttributeError:
                                    has_media = False
                                except IndexError:
                                    break

                        try:
                            story = autofiller[auto_index]
                        except IndexError:
                            break

                        context[placeholder.name].append(story.child)
                        placed.append(story.pk)
                        auto_index += 1

        return context

    def defined_placeholders(self):
        return [ph['node'] for ph in
                placeholders.get_placeholder_list(self.parent.template_path)]

    def save(self, *args, **kwargs):
        super(LayoutInstance, self).save(*args, **kwargs)
        ph_items = self.defined_placeholders()
        for ph in ph_items:
            types = re.sub(r'[ ]?,[ ]?', ',', ph.content_types).split(',')
            types = [ContentType.objects.get(app_label='content',
                                             model=t.lower().replace(' ', ''))
                                        .model_class()
                     for t in types]
            num = len(self.placeholders.filter(name=ph.name))
            if num == 0:
                ph_obj = Placeholder(layout=self, name=ph.name)
            elif num > 1:
                raise Exception(
                    'Multiple placeholders saved for name %s' % (ph.name,))
            else:
                ph_obj = self.placeholders.get(name=ph.name)

            ph_obj.min_items = ph.content_range['min']
            ph_obj.save()

    def __unicode__(self):
        return self.name


class Placeholder(models.Model):
    layout = models.ForeignKey(LayoutInstance, related_name='placeholders')
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=50, blank=True)
    title_link = models.CharField(max_length=100, blank=True)
    extra_text = models.TextField(blank=True)
    min_items = models.IntegerField(null=True, blank=True)
    # should have max items, content_types
    position = models.IntegerField(
        null=True, blank=True)  # for autofill ordering
    autofill_tags = models.ManyToManyField(
        'content.Tag', blank=True, related_name='placeholders')
    autofill_section = models.ForeignKey(
        'content.Section', null=True, blank=True, related_name='placeholders')
    autofill_prioritize = models.BooleanField(default=False)
    autofill_number = models.IntegerField(null=False, default=0)
    autofill_contenttypes = models.ManyToManyField(
        ContentType, blank=True)
    require_media = models.BooleanField(default=False)
    # add autofill M2M on content type?

    @property
    def content(self):
        """ This method evaluates the QuerySet and returns a list """
        return [cr.content for cr in self.content_relations.all()]

    @property
    def rel_admin_content(self):
        return ';'.join(
            str(x.content.pk) for x in self.content_relations.all())

    @property
    def node(self):
        try:
            return placeholders.find_placeholder(
                self.layout.parent.template_path,
                self.name
            )['node']
        except:
            return None

    def valid_types(self):
        """Returns a list of valid types (represented as strings)"""
        types = re.sub(r'[ ]?,[ ]?', ',', self.node.content_types).split(',')
        return [t.lower() for t in types]

    def get_autofiller(self):
        """
        Set up an autofiller QuerySet for use in Layout rendering. This
        can be overridden in a subclass of Placeholder to provide some
        specialized autofilling procedure. All this needs to do is return
        a QuerySet that contains items in the order they should be autofilled.
        """
        constraint = Q(content_type__in=self.autofill_contenttypes.all())
        if self.autofill_tags.count() > 0:
            constraint &= Q(tags__in=self.autofill_tags.all())
        if self.autofill_section:
            constraint &= Q(section=self.autofill_section)
        # NOTE: already placed objects are removed from this QuerySet in
        # Layout.get_context

        if self.autofill_prioritize:
            for n in [25, 50, 100, 200, 400]:
                autofiller = Content.objects.prioritized(n).filter(constraint)
                if len(autofiller) >= self.autofill_number:
                    break
        else:
            autofiller = Content.objects.order_by('-issue__issue_date') \
                                        .filter(constraint)

        return autofiller

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        if self.min_items is not None and self.min_items != 0:
            try:
                if self.min_items < self.node.content_range['min']:
                    raise IntegrityError(
                        'Placeholder %s has a minimum of %d objects, please '
                        'set the minimum to at least %d' % (
                            self.placeholder.name,
                            self.node.content_range['min'],
                            self.node.content_range['min'],
                        )
                    )
                if self.min_items > self.node.content_range['max']:
                    raise IntegrityError(
                        'Placeholder %s has a maximum of %d objects, please '
                        'set the minimum to at most %d' % (
                            self.placeholder.name,
                            self.node.content_range['max'],
                            self.node.content_range['max'],
                        )
                    )
            except:
                pass

        is_new = not self.pk

        super(Placeholder, self).save(*args, **kwargs)

        # autofill on all content types by default
        if is_new and not self.autofill_contenttypes.count():
            self.autofill_contenttypes.add(
                *[ContentType.objects.get(app_label='content',
                                          model=c.replace(' ', ''))
                  for c in self.valid_types()])

    class Meta:
        unique_together = (('layout', 'name'), ('layout', 'position'))


class PlaceholderContentRelation(models.Model):
    placeholder = models.ForeignKey(
        Placeholder, related_name='content_relations')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()  # for GenericForeignKey
    position = models.IntegerField()
    content = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.placeholder.__unicode__()

    def save(self, *args, **kwargs):
        # placeholder size validation:
        try:
            max_content = self.placeholder.node.content_range['max']
            is_new = self.placeholder.content_relations.filter(pk=self.pk) \
                                                       .count() == 0
            curr_content = self.placeholder.content_relations.count()
            if is_new and curr_content >= max_content:
                raise IntegrityError(
                    'Placeholder %s can only hold %d objects' % (
                        self.placeholder.name, max_content))
        except TypeError:
            pass  # there was no content_range specified

        # type validation:
        try:
            valid_types = self.placeholder.valid_types()
            if (not self.content_type.name.lower() in valid_types and
                    not(self.content_type.name == 'external content' and
                        self.content.repr_type.name in valid_types)):
                raise IntegrityError(
                    'Placeholder %s can\'t hold `%s` objects' % (
                        self.placeholder.name, self.content_type.name))
        except TypeError:
            pass  # there were no specified content types

        # TODO position validation

        return super(PlaceholderContentRelation, self).save(*args, **kwargs)

    class Meta:
        ordering = ['position']
        unique_together = ('placeholder', 'position')
