from django.shortcuts import render

def home_view(request):
	user = request.user
	ctx = {
		'user':user,
		'hello':'Hello World'
	}
	return render(request, 'main/home.html', ctx)