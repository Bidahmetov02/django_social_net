from django.shortcuts import render
from .models import Profile, Relationship
from .forms import ProfileModelForm

# Create your views here.
def my_profile_view(request):
	profile = Profile.objects.get(user=request.user)
	form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
	confirm = False

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			confirm = True

	ctx = {
		'profile': profile,
		'form': form,
		'confirm': confirm,
	}

	return render(request, 'profiles/myprofile.html', ctx)

def invites_received_view(request):
	profile = Profile.objects.get(user=request.user)
	qs = Relationship.objects.invatations_received(profile)

	ctx = {
		'qs': qs
	}

	return render(request, 'profiles/my_invites.html', ctx)

def profiles_list_view(request):
	user = request.user
	qs = Profile.objects.get_all_profiles(user)

	ctx = {
		'qs': qs
	}

	return render(request, 'profiles/profile_list.html', ctx)

def invite_profiles_list_view(request):
	user = request.user
	qs = Profile.objects.get_all_profiles_to_invite(user)

	ctx = {
		'qs': qs
	}

	return render(request, 'profiles/to_invite_list.html', ctx)
