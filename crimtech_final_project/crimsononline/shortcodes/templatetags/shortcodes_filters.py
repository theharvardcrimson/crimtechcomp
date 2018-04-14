from django import template

from crimsononline.shortcodes import parser

register = template.Library()


def shortcodes_replace(value):
    return parser.parse(value)


register.filter('shortcodes', shortcodes_replace)
