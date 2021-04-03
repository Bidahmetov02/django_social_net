from django.urls import path
from .views import (
	my_profile_view, 
	invites_received_view, 
	# invite_profiles_list_view, 
	ProfileListView,
	send_invatation,
	remove_from_friends,
	accept_invatation,
	reject_invatation,
	ProfileDetailView,
	my_friends_view, 
	search_view
)

app_name = 'profiles'

urlpatterns = [
	path('', ProfileListView.as_view(), name="all-profiles-view"),
	path('myprofile/', my_profile_view, name="my-profile-view"),
	path('my-friends/', my_friends_view, name="my_friends_view"),
	path('my-invites/', invites_received_view, name="invites-received-view"),
	# path('to-invite/', invite_profiles_list_view, name="invite-profiles-view"),
	path('send-invite/', send_invatation, name="send-invite"),
	path('remove-friend/', remove_from_friends, name="remove-friend"),
	path('my-invites/accept', accept_invatation, name="accept-invite"),
	path('my-invites/reject', reject_invatation, name="reject-invite"),
	path('<slug>', ProfileDetailView.as_view(), name='profile-detail-view'),
	path('search/', search_view, name="search_view")
]