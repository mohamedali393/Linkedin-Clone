from django.urls import path
from . import views


urlpatterns = [
    path('create-post/',views.CreatePostView.as_view(),name='create-post'),
    path('post/<str:pk>/',views.post_details,name='post-detail'),
    path('update-post/<str:pk>/',views.UpdatePostView.as_view(),name='update-post'),
    path('update-comment/<str:pk>/',views.UpdateCommentView.as_view(),name='update-comment'),
    path('delete-comment/<str:pk>/',views.DeleteCommentView.as_view(),name='delete-comment'),
    path('like-post/<str:pk>/',views.LikePost.as_view(),name='like-post'),
    path('search/',views.search,name='search'),
    path('replay-comment/<str:pk>/',views.replay_comment,name='replay-comment'),
    path('share_post/<str:pk>/',views.share_post,name='share-post'),
]