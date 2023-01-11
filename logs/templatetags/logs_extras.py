from django import template
from django.contrib.admin.templatetags import admin_list

register = template.Library()


@register.inclusion_tag('log/pagination_log.html', takes_context=True)
def custom_pagination_log(context, cl):
    pagination = admin_list.pagination(cl)
    return pagination


@register.inclusion_tag('log/search_form_log.html',  takes_context=True)
def custom_search_form_log(context, cl):
    search_form = admin_list.search_form(cl)
    return search_form
