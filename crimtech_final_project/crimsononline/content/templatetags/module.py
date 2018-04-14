from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()


class ModuleNode(template.Node):
    """
    WARNING: The below comment is entirely out of date. I don't know
    what this "module" does (nice name choice, dude), but it certainly
    doesn't make a rotator.

    Generates a rotator.
    2 required arguments:
        @contents => list of content to rotate
        @id => unique (for the page) id.  used as 'id' attribute in html
    Optional:
        @title => a title (displayed at the top)
    """
    def __init__(self, nodelist, title, width, color, link):
        self.nodelist = nodelist
        self.width = width
        self.color = color
        self.link = link
        try:
            self.title = template.Variable(title)
        except:
            self.title = title

    def render(self, context):
        try:
            real_title = self.title.resolve(context).upper()
        except:
            real_title = str(self.title).upper()
        if self.link:
            real_title = mark_safe(
                '<a href="%s">%s</a>' % (self.link, real_title))
        cont = mark_safe(self.nodelist.render(context))
        return render_to_string(
            'templatetag/module.html',
            {'c': cont, 'title': real_title, 'width': self.width,
             'color': self.color})


def do_module(parser, token):
    tokens = token.split_contents()
    if len(tokens) < 3:
        raise template.TemplateSyntaxError, \
            '%r tag takes at least 3 arguments' % tokens[0]
    width = tokens[1]
    title = tokens[2] if tokens[2][0] not in ("'", '"') \
        else tokens[2][1:len(tokens[2]) - 1]
    color = tokens[3] if len(tokens) >= 4 else 'blue'
    link = tokens[4] if len(tokens) >= 5 else ''
    if link and link[0] in ("'", '"'):
        link = link[1:-1]
    nodelist = parser.parse(('endmodule',))
    parser.delete_first_token()
    return ModuleNode(nodelist, title, width, color, link)


register.tag('module', do_module)
