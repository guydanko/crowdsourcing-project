from django import template

register = template.Library()


@register.filter(name='get_duration')
def duration(td):
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return '{}:{}'.format(minutes, seconds)
