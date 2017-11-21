from django import template
from django.core.urlresolvers import reverse
from django.urls.exceptions import NoReverseMatch

register = template.Library()


@register.simple_tag
def is_active(request, url, side_nav=None, key=None, arg=None):
    # Main idea is to check if the url and the current path is a match
    try:
        if arg:
            key = str(key)
            if reverse(url, kwargs={key: arg}) == request.path == '/':
                return "active"
            if reverse(url, kwargs={key: arg}) != '/' and request.path != '/':
                if request.path == reverse(url, kwargs={key: arg}):
                    return "active"
                if reverse(url, kwargs={key: arg}) in request.path and side_nav:
                    return ""
                if reverse(url, kwargs={key: arg}) in request.path:
                    return "active"
            return ""
        else:
            if reverse(url) == request.path == '/':
                return "active"
            if reverse(url) != '/' and request.path != '/':
                if request.path == reverse(url):
                    return "active"
                if reverse(url) in request.path and side_nav:
                    return ""
                if reverse(url) in request.path:
                    return "active"
            return ""
    except NoReverseMatch:
        return ""


@register.filter
def author(books, auth):
    return books.filter(author=auth)
