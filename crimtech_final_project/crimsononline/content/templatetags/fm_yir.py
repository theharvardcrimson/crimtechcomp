import logging

from django import template
from django.template import Node

logger = logging.getLogger(__name__)
register = template.Library()


@register.filter
def yir_img(content):
    if content.__class__.__name__ == 'Article':
        return content.main_rel_content
    elif content.__class__.__name__ == 'Gallery':
        return content.cover_image


@register.filter
def firstthird(lst):
    return lst[:len(lst) / 3 + 1]


@register.filter
def remthird(lst):
    return lst[len(lst) / 3 + 1:]


class SplitListNode(Node):
    def __init__(self, list_string, chunk_size, new_list_name):
        self.list = list_string
        self.chunk_size = chunk_size
        self.new_list_name = new_list_name

    def split_seq(self, seq, size):
        """ Split up seq in pieces of size, from
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/425044"""
        return [seq[i:i + size] for i in range(0, len(seq), size)]

    def render(self, context):
        context[self.new_list_name] = self.split_seq(context[self.list],
                                                     int(self.chunk_size))
        return ''


def group_list(parser, token):
    """<% split_list list as new_list 5 %>"""
    bits = token.contents.split()
    if len(bits) != 5:
        raise Exception('Syntax Error in Grouping List')
    return SplitListNode(bits[1], bits[4], bits[3])


register.tag('group_list', group_list)
