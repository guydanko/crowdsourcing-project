from django import template

register = template.Library()


@register.filter(name='get_duration')
def duration(td):
    hours = td.hour
    minutes = td.minute
    seconds = td.second
    if seconds < 10:
        seconds = "0" + str(seconds)
    if minutes < 10:
        minutes = "0" + str(minutes)
    if hours < 10:
        hours = "0" + str(hours)
    return '{}:{}:{}'.format(hours, minutes, seconds)


@register.filter(name='index')
def index(sequence, position):
    return sequence[position]


@register.filter(name='equal')
def equal(obj1, obj2):
    return obj1 == obj2
