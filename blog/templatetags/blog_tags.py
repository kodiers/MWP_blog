from django import template

from django.contrib.auth.models import User

register = template.Library()


@register.inclusion_tag('blog/random_users.html')
def random_authors(count=5):
    """
    Get 5 random authors and show in random_users template
    """
    authors = User.objects.all().order_by('?')[:count]
    return {'authors': authors}


@register.filter()
def add_class_to_formfield(field, css):
    """
    Filter to add CSS class to form field
    """
    return field.as_widget(attrs={"class": css})