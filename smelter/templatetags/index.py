from django import template
register = template.Library()

@register.filter
def index(List, i):
	try:
		return List[int(i)]
	except IndexError:
		return "Empty"
