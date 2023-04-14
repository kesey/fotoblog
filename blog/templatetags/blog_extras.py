from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def model_type(instance): # custom filter
    return type(instance).__name__

@register.filter
def get_posted_at_display(time):
    time_passed = timezone.now() - time
    if timedelta(minutes=0) < time_passed < timedelta(minutes=60):
        return f"Posté il y a {(time_passed.total_seconds % 3600) // 60} minutes"
    elif timedelta(hours=1) < time_passed < timedelta(hours=24):
        return f"Posté il y a {time_passed.total_seconds // 3600} heures"
    elif time_passed > timedelta(hours=24):
        return f"Publié le {time.strftime('%H:%M %d %b %y')}"

@register.simple_tag(takes_context=True)
def get_poster_display(context, user): # custom balise
    if context["user"] == user:
        return "vous"
    return user.username
