from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
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

@login_required
def invites_received_view(request):
	profile = Profile.objects.get(user=request.user)
	qs = Relationship.objects.invatations_received(profile)
	results = list(map(lambda x: x.sender, qs))
	is_empty = False
	if len(results) == 0:
		is_empty = True

	ctx = {
		'qs': results,
		'is_empty': is_empty
	}

	return render(request, 'profiles/my_invites.html', ctx)

def search_view(request):
	sr = request.GET.get('q')
	is_empty = False

	first_name = set(Profile.objects.filter(first_name__icontains = sr))
	last_name = set(Profile.objects.filter(last_name__icontains = sr))
	usernames = set(User.objects.filter(username__icontains = sr))

	results = first_name | last_name

	for n in usernames:
		temp = Profile.objects.get(user=n)
		results.add(temp)

	if results == 0:
		is_empty = False

	print(results)

	ctx = {
		'results': results,
		'is_empty': is_empty,
		'lookup': sr,
	}

	return render(request, 'profiles/search_results.html', ctx)

@login_required
def profiles_list_view(request):
	user = request.user
	qs = Profile.objects.get_all_profiles(user)

	ctx = {
		'qs': qs
	}

	return render(request, 'profiles/profile_list.html', ctx)

@login_required
def my_friends_view(request):
	user = request.user
	is_empty = False
	qs = Profile.get_friends(user)
	if len(qs) == 0:
		is_empty = True

	ctx = {
	'qs':qs, 
	'is_empty': is_empty,
	}

	return render(request, 'profiles/my_friends.html', ctx)

@login_required
def accept_invatation(request):
	if request.method == "POST":
		pk = request.POST.get("profile_pk")
		sender = Profile.objects.get(pk=pk)
		receiver = Profile.objects.get(user=request.user)
		rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
		if rel.status == "sent":
			rel.status = 'accepted'
			rel.save()

	return redirect('profiles:invites-received-view')

@login_required
def reject_invatation(request):
	if request.method == "POST":
		pk = request.POST.get("profile_pk")
		sender = Profile.objects.get(pk=pk)
		receiver = Profile.objects.get(user=request.user)
		rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
		rel.delete()
		
	return redirect('profiles:invites-received-view')

# @login_required
# def invite_profiles_list_view(request):
# 	user = request.user
# 	qs = Profile.objects.get_all_profiles_to_invite(user)

# 	ctx = {
# 		'qs': qs
# 	}

# 	return render(request, 'profiles/to_invite_list.html', ctx)

class ProfileDetailView(LoginRequiredMixin, DetailView):
	model = Profile
	template_name = 'profiles/detail.html'

	def get_object(self, **kwargs):
		slug = self.kwargs.get('slug')
		profile = Profile.objects.get(slug=slug)

		return profile

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    user = User.objects.get(username__iexact=self.request.user)
	    profile = Profile.objects.get(user=user)
	    rel_r = Relationship.objects.filter(sender=profile)
	    rel_s = Relationship.objects.filter(receiver=profile)
	    rel_receiver = []
	    rel_sender = []

	    for item in rel_r:
	    	rel_receiver.append(item.receiver.user) 

	    for item in rel_s:
	    	rel_sender.append(item.sender.user)

	    context['rel_receiver'] = rel_receiver
	    context['rel_sender'] = rel_sender
	    context['posts'] = self.get_object().get_all_authors_posts()
	    context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False

	    return context

class ProfileListView(LoginRequiredMixin, ListView):
	model = Profile
	template_name = 'profiles/profile_list.html'
	context_object_name = 'qs'

	def get_queryset(self):
		qs = Profile.objects.get_all_profiles(self.request.user)

		return qs

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    user = User.objects.get(username__iexact=self.request.user)
	    profile = Profile.objects.get(user=user)
	    rel_r = Relationship.objects.filter(sender=profile)
	    rel_s = Relationship.objects.filter(receiver=profile)
	    rel_receiver = []
	    rel_sender = []

	    for item in rel_r:
	    	rel_receiver.append(item.receiver.user) 

	    for item in rel_s:
	    	rel_sender.append(item.sender.user)

	    context['rel_receiver'] = rel_receiver
	    context['rel_sender'] = rel_sender
	    context['is_empty'] = False
	    if len(self.get_queryset()) == 0:
	    	context['is_empty'] = True

	    return context

@login_required
def send_invatation(request):
	if request.method == 'POST':
		pk = request.POST.get("profile_pk")
		user = request.user
		sender = Profile.objects.get(user=user)
		receiver = Profile.objects.get(pk=pk)

		rel = Relationship.objects.create(sender=sender, receiver=receiver, status='sent')

		return redirect(request.META.get('HTTP_REFERER'))
	
	return redirect('profiles:my-profile-view')

@login_required
def remove_from_friends(request):
	if request.method == 'POST':
		pk = request.POST.get("profile_pk")
		user = request.user
		sender = Profile.objects.get(user=user)
		receiver = Profile.objects.get(pk=pk)

		rel = Relationship.objects.get(
			(Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)))
		rel.delete()

		return redirect(request.META.get('HTTP_REFERER'))
	
	return redirect('profiles:my-profile-view')




