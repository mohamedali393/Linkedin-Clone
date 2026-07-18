from django.urls import path
from . import views


urlpatterns = [
    path('',views.groups,name='groups'),
    path('create-group/',views.create_group,name='create-group'),
    path('group-detail/<str:pk>/',views.group_detail,name='group-detail'),
    path('join-group/<str:pk>/',views.join_group,name='join-group'),
    path('accept-group-request/<str:pk>/',views.accept_group_request,name='accept-group-request'),
    path('reject-group-request/<str:pk>/',views.reject_group_request,name='reject-group-request'),
    path('leave-group/<str:pk>/',views.leave_group,name='leave-group'),
    path('like-post-group/<str:pk>/',views.like_post_group,name='like-post-group'),
    path('group-post-detail/<str:pk>/',views.group_post_detail,name='group-post-detail'),
]