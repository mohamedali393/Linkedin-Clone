from django.urls import path
from . import views


urlpatterns = [
    path('',views.my_notifications,name='my-notifications'),
    path('redirect-notification/<str:pk>/',views.redirect_notification,name='redirect-notification'),
]