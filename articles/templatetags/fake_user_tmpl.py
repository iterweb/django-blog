from django.template import Library
from random import randint
from datetime import datetime


register = Library()

night = 235922861933
morning = 100129385257
current_time = str(datetime.now().time()).replace(':', '').replace('.', '')


@register.simple_tag
def fake_user_count():

    if morning < int(current_time):
        f = randint(1, 9)
        h = 187 - f
        return str(h)

    elif night > int(current_time):
        f = randint(1, 4)
        h = 58 - f
        return str(h)
