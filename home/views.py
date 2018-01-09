from django.shortcuts import render

# Create your views here.
def index(request):
	if request.session.has_key('username'):
		firstName = request.session['firstname']

		return render(request, 'home/home.html',
			{'firstName': firstName})

	return render(request, 'home/home.html', { })
	