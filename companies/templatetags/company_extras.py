from django import template
from django.template.context import Context

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
