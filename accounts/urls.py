from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.register,name='register'),
    path('',views.user_account,name='account'),
    path('update-profile/',views.update_profile,name='update-profile'),
    path('create-skill/',views.create_skill,name='create-skill'),
    path('create-education/',views.create_education,name='create-education'),
    path('create-experience/',views.create_experience,name='create-experience'),
    path('create-language/',views.create_language,name='create-language'),
    path('profile/<str:pk>/',views.profile_details,name='profile'),
    path('connections-requests/',views.my_connections_requests,name='my-connections-requests'),
    path('create-connection/<str:reciver_id>/',views.create_connection,name='create-connection'),
    path('accept-connection/<str:pk>/',views.accept_user_connection,name='accept-connection'),
    path('reject-connection/<str:pk>/',views.reject_user_connection,name='reject-connection'),
    path('remove-user-connection/<str:pk>/',views.delete_connection,name='remove-connection'),
]