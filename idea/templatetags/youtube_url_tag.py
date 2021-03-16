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

@register.simple_tag
def ppt_url(ppt_link):
    if 'pub?' in ppt_link:
        ppt_id = ppt_link.split('pub?')[0]
        ppt_embed_link = ppt_id + 'embed?start=false&loop=false&delayms=3000'
    elif 'embed?' in ppt_link:
        ppt_embed_link = ppt_link
    else:
        ppt_embed_link = ''
    return ppt_embed_link
