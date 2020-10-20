from django.template import Library
from articles.models import Post


register = Library()


@register.simple_tag
def count_posts():
    all_posts_count = Post.objects.all().count()
    return all_posts_count