# TODO: rename this file shortcuts
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.http import Http404


def paginate(queryset, page_num, items_per_page, four_oh_four=True):
    """
    Takes a possibly bad page_num and paginates.
    Returns a dictionary that can directly be used in the context:
        {'p': page obj, 'paginator': paginator obj, 'content': object list}
    @queryset => paginates across this queryset
    @page_num => the number of the page (first page?, second page?)
    @items_per_page => duh
    @four_oh_four => if True, throws a 404 when page is invalid, otherwise
        throws the real error
    """
    if not page_num:
        page_num = 1
    p = Paginator(queryset, items_per_page)
    try:
        page = int(page_num)
        page = p.page(page)
    except (ValueError, EmptyPage, InvalidPage):
        if four_oh_four:
            raise Http404
        raise
    return {'p': page, 'paginator': p, 'content': page.object_list}
