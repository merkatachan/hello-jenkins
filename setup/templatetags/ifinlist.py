from django import template
register = template.Library()

@register.filter
def ifinlist(value, plist):
	return True if value in plist else False
