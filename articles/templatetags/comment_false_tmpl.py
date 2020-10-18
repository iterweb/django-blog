from django import template
from articles.models import Comment


register = template.Library()


@register.inclusion_tag('template_tags/comment_false.html')
def comments_false():
    comment_false = Comment.objects.filter(published=False)[:10]
    comment_count = Comment.objects.filter(published=False).count()
    return {
        'comment_false': comment_false,
        'comment_count': comment_count,
    }