from django import template

register = template.Library()


@register.simple_tag
def complete(file1, file2, file3, file4):
    complete_rate = 0
    if file1:
        complete_rate += 50
    if file2:
        complete_rate += 16.7
    if file3:
        complete_rate += 16.7
    if file4:
        complete_rate += 16.7
    if file1 and file2 and file3 and file4:
        complete_rate = 100
    return complete_rate
