import logging
import re

from django import template
from django.conf import settings

logger = logging.getLogger(__name__)

register = template.Library()


@register.tag('placeholder')
def do_placeholder(parser, token):
    """
    Usage:
     {% placeholder name="test1" content_range="(1, 5)"
        content_types="article, image" as test_items %}
     if there is no "as test_items" part, the content array gets put in
     `placeholder_items`.
    """

    # parses until {% endplaceholder %}
    nodelist = parser.parse(('endplaceholder'),)
    # deletes the {% endplaceholder %} token
    parser.delete_first_token()
    data = parse_args(token.contents)
    return PlaceholderNode(nodelist, **data)


class PlaceholderNode(template.Node):
    """
    Note that this is dependent upon the context having
    a `crimsononline.layout` key set
    """
    def __init__(self, nodelist, name, content_range=None, content_types=None,
                 context_var='placeholder_items'):
        self.name = name
        self.content_range = content_range  # dict with 'min' and 'max' keys
        self.content_types = content_types
        self.context_var = context_var
        self.nodelist = nodelist

    @staticmethod
    def follow_nodes(nodes, level):
        for node in nodes:
            print('\t' * level + str(node))
            try:
                PlaceholderNode.follow_nodes(node.nodelist, level + 1)
            except:
                pass

    def render(self, context):
        try:
            layout_obj = context['crimsononline.layout']
        except KeyError:
            return ''  # we weren't placeholder-ified, fail silently

        # self.follow_nodes(self.nodelist, 0)

        # NOTE: in future versions of django, we can do: "with context.push():"
        #       to auto-call context.pop(). this is called a context manager.
        try:
            context.push()
            context[self.context_var] = context[layout_obj][self.name]
            r = self.nodelist.render(context)
            context.pop()
            return r
        except KeyError:
            context.pop()
            if settings.TEMPLATE_DEBUG:
                raise Exception('Placeholder %s not found in db' % self.name)
            else:
                return ''  # no placeholder found in db, fail silently


# possibly use the token.split_args() method to help this? or shlex
def parse_args(args):
    # From shortcodes.parser
    regex = re.compile(r'[ ]*(\w+)[ ]?=[ ]?([^" ]+|"[^"]*")[ ]*(?: |$)')
    groups = regex.findall(args)
    parsed_args = {}

    for group in groups:
        if len(group) == 2:
            item_key = group[0]
            item_value = group[1]

            if item_value.startswith('"') and item_value.endswith('"'):
                # Strip quotes
                item_value = item_value[1:-1]
        parsed_args[item_key] = item_value

    if 'content_range' in parsed_args:
        range_regex = re.compile(r'[ ]*\([ ]*(\d+)[ ]*,[ ]*(\d+)[ ]*\)')
        range_groups = range_regex.findall(parsed_args['content_range'])

        if range_groups and len(range_groups[0]) == 2:
            min_range = 0
            max_range = 0

            try:
                min_range = int(range_groups[0][0])
            except (ValueError, IndexError):
                min_range = 0
            try:
                max_range = int(range_groups[0][1])
            except (ValueError, IndexError):
                max_range = 9999

            parsed_args['content_range'] = {
                'min': min_range,
                'max': max_range
            }

    try:
        splargs = args.split()
        parsed_args['context_var'] = splargs[splargs.index('as') + 1]
    except ValueError:
        pass

    return parsed_args


def get_placeholder_list(template_ob, flat=False):
    if template_ob.__class__ == str or template_ob.__class__ == unicode:
        template_ob = template.loader.get_template(template_ob).template
    return __get_placeholder_list(template_ob, flat)


def __get_placeholder_list(root_node, flat):
    placeholder_list = []
    for node in root_node.nodelist:
        if node.__class__ == PlaceholderNode:
            if not flat:
                data = {
                    'node': node,
                    'children': __get_placeholder_list(node, flat)
                }
            else:
                data = {'node': node}
                placeholder_list += __get_placeholder_list(node, flat)
            placeholder_list.append(data)

        elif hasattr(node, 'nodelist'):
            placeholder_list += __get_placeholder_list(node, flat)

    return placeholder_list


def find_placeholder(template_ob, name):
    parsed_list = get_placeholder_list(template_ob)
    return __find_placeholder_recursive(parsed_list, name)


def __find_placeholder_recursive(parsed_list, name):
    for d in parsed_list:
        if d['node'].name == name:
            return d
        else:
            potential_node = __find_placeholder_recursive(d['children'], name)
            if potential_node:
                return potential_node

    return None


@register.tag('ph_info')
def do_ph_info(parser, token):
    """
    Usage:
     {% ph_info name="test1" as test_info %}
     if there is no "as test_info" part, the info dict gets put in
     `placeholder_info`.
    """

    nodelist = parser.parse(('endinfo'),)  # parses until {% endinfo %}
    parser.delete_first_token()  # deletes the {% endinfo %} token
    data = parse_args(token.contents)
    return PlaceholderInfoNode(nodelist, **data)


class PlaceholderInfoNode(template.Node):
    """
    Note that this is dependent upon the context having
    a `crimsononline.layout` key set
    """
    def __init__(self, nodelist, name, context_var='placeholder_info'):
        self.name = name
        self.context_var = context_var
        self.nodelist = nodelist

    def render(self, context):
        layout_obj = context['crimsononline.layout']

        resp = context[layout_obj][self.name]
        resp.count = len(context[layout_obj][self.name])

        # NOTE: in future versions of django, we can do: "with context.push():"
        #       to auto-call context.pop(). this is called a context manager.
        try:
            context.push()
            context[self.context_var] = resp
            r = self.nodelist.render(context)
            context.pop()
            return r
        except KeyError:
            context.pop()
            if settings.TEMPLATE_DEBUG:
                raise Exception('Placeholder %s not found in db' % self.name)
            else:
                return ''  # no placeholder found in db, fail silently
