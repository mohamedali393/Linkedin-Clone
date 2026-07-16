from django.urls import path
from . import views


urlpatterns = [
    path('create-conversation/<str:pk>/',views.create_conversation,name='create-conversation'),
    path('conversation/<str:pk>/',views.conversation_detail,name='conversation'),
    path('messaging/',views.messagings,name='messagings'),
]