from django import template

register = template.Library()


@register.filter(name='get_duration')
def duration(td):
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    if seconds < 10:
        seconds = "0" + str(seconds)

    return '{}:{}'.format(minutes, seconds)
