from django import template

register = template.Library()

@register.filter
def is_saved(job, saved_jobs):
    return saved_jobs.filter(job=job).exists()