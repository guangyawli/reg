from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_url(org_url):
    url = org_url
    if 'https://youtu.be/' in org_url:
        video_id = org_url.split('/')[-1]
        url = 'https://www.youtube.com/embed/' + video_id
    if '/watch?v=' in org_url:
        if '&' in org_url:
            org_url = org_url.split('&')[0]
        video_id = org_url.split('/')[-1].split('=')[-1]
        url = 'https://www.youtube.com/embed/' + video_id
    return url
