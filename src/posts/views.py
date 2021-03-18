from django.shortcuts import render, redirect
from .models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
# Create your views here.

def post_comment_create_and_list_view(request):
	qs = Post.objects.all()
	profile = Profile.objects.get(user=request.user)
 
	p_form = PostModelForm()
	c_form = CommentModelForm()
	post_added = False

	if 'submit_p_form' in request.POST:
		p_form = PostModelForm(request.POST, request.FILES)
		if p_form.is_valid():
			ins = p_form.save(commit=False)
			ins.author = profile
			ins.save()
			p_form = PostModelForm()
			post_added = True

	if 'submit_c_form' in request.POST:
		c_form = CommentModelForm(request.POST)
		if c_form.is_valid():
			ins = c_form.save(commit=False)
			ins.user = profile
			ins.post = Post.objects.get(id=request.POST.get('post_id'))
			ins.save()
			c_form = CommentModelForm()


	ctx = {
		'qs': qs,
		'profile': profile,
		'p_form': p_form,
		'c_form': c_form,
		'post_added': post_added,
	}

	return render(request, 'posts/main.html', ctx)

def like_unlike_post(request):
	user = request.user
	if request.method == "POST":
		post_id = request.POST.get('post_id')
		post_obj = Post.objects.get(id=post_id)
		profile = Profile.objects.get(user=user)

		if profile in post_obj.liked.all():
			post_obj.liked.remove(profile)
		else:
			post_obj.liked.add(profile)

		like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

		if not created:
			if like.value == 'Like':
				like.value = 'Unlike'
			else:
				like.value = 'Like'
		else:
			like.value = 'Like'

			post_obj.save()
			like.save()

	return redirect('posts:main-post-view')
