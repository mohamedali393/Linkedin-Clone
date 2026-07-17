from django.urls import path
from . import views


urlpatterns = [
    path('all-tags/',views.all_tags,name='all-tags'),
    path('',views.index,name='index'),
    path('<str:tag_name>/',views.index,name='posts-by-tag'),
    path('jobs/',views.jobs_page,name='jobs'),
    path('create-company/',views.create_company,name='create-company'),
    path('my-companies/',views.my_companies,name='my-companies'),
    path('company-details/<str:pk>/',views.company_details,name='company-details'),
    path('update-company/<str:pk>/',views.update_company,name='update-company'),
    path('create-job/<str:pk>/',views.create_job,name='create-job'),
    path('create-new-job/',views.post_new_job,name='create-new-job'),
    path('delete-company/<str:pk>/',views.delete_company,name='delete-company'),
    path('job-aplie/<str:pk>/',views.applie_job,name='applie-job'),
    path('my-applications/',views.my_applications,name='my-applications'),
    path('job/<str:pk>/',views.job_details,name='job'),
    path('job-applications/<str:pk>/',views.job_applications,name='job-applications'),
    path('update-job/<str:pk>/',views.update_job,name='update-job'),
    path('delete-job/<str:pk>/',views.delete_job,name='delete-job'),
    path('accept-job-application/<str:pk>/',views.accept_job_application,name='accept-job-application'),
    path('reject-job-application/<str:pk>/',views.reject_job_application,name='reject-job-application'),
]