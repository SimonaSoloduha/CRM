from django import template
from django.template.context import Context
from django.contrib.admin.templatetags import admin_list

register = template.Library()


@register.inclusion_tag('company/submit_line.html', takes_context=True)
def custom_submit_row(context):
    ctx = Context(context)
    ctx.update(
        {
            "show_delete_link": context.get("show_delete", True),
        }
    )
    return ctx


@register.inclusion_tag('company/pagination_company.html', takes_context=True)
def custom_pagination_company(context, cl):
    pagination = admin_list.pagination(cl)
    return pagination


@register.inclusion_tag('company/search_form_company.html',  takes_context=True)
def search_form_company(context, cl):
    search_form = admin_list.search_form(cl)
    return search_form
