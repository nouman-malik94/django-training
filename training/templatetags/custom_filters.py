from django import template
register = template.Library()



@register.filter(name='add_class')
def add_class(field, css_class):
    if field.field.widget.attrs.get('class'):
        classes = field.field.widget.attrs['class'] + f' {css_class}'
    else:
        classes = css_class
    return field.as_widget(attrs={'class': classes})
