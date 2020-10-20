from django.template import Library
from articles.models import Post


register = Library()


@register.inclusion_tag('template_tags/post_false.html')
def posts_false():
    post_false = Post.objects.filter(is_published=False)[:10]
    posts_count = Post.objects.filter(is_published=False).count()
    return {
        'post_false': post_false,
        'posts_count': posts_count,
    }