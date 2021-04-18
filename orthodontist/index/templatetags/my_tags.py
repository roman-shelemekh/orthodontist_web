from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def highlight_search(text, search_input):
    search_input= re.escape(search_input)
    print(search_input)
    # search_input = '|'.join(str(search_input).split())
    text = str(text)
    pattern = re.compile(search_input, re.IGNORECASE)
    highlighted = pattern.sub('<span style="background-color: #00F5C8;">\g<0></span>', text)
    return mark_safe(highlighted)
