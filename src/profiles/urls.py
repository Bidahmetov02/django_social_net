from django.urls import path
from .views import (
	my_profile_view, 
	invites_received_view, 
	invite_profiles_list_view, 
	ProfileListView,
	send_invatation,
	remove_from_friends
)

app_name = 'profiles'

urlpatterns = [
	path('myprofile/', my_profile_view, name="my-profile-view"),
	path('my-invites/', invites_received_view, name="invites-received-view"),
	path('all-profiles/', ProfileListView.as_view(), name="all-profiles-view"),
	path('to-invite/', invite_profiles_list_view, name="invite-profiles-view"),
	path('send-invite/', send_invatation, name="send-invite"),
	path('remove-friend/', remove_from_friends, name="remove-friend"),

]