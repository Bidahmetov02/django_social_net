from django.shortcuts import render
from .models import Profile

# Create your views here.
def my_profile_view(request):
	profile = Profile.objects.get(user=request.user)
	ctx = {
		'profile':profile,
	}
	return render(request, 'profiles/myprofile.html', ctx)
