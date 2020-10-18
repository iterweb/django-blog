from django import template
from django.db.models import Count, F

from articles.models import Category


register = template.Library()


@register.inclusion_tag('template_tags/menu.html')
def show_categories():
    categories = Category.objects.annotate(cnt=Count('posts', filter=F('posts__is_published'))).filter(cnt__gt=0)
    return {
        'categories': categories,
    }
