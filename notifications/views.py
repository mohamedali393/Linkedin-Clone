from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification
from contact.models import Conversation
from accounts.models import ConnectionRequest
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def my_notifications(request):
    notifications = Notification.objects.filter(receiver=request.user,is_read=False)

    context = {
        'notifications': notifications,
    }
    return render(request,'notifications/notifications.html',context)


@login_required(login_url='login')
def redirect_notification(request,pk):
    notification = get_object_or_404(Notification,pk=pk,receiver=request.user)
    notification.is_read = True
    notification.save()

    if notification.notification_type == 'like':
        return redirect('post-detail',pk=notification.post.id)
    
    if notification.notification_type == 'job_application':
        return redirect('job',pk=notification.job.id)
    
    if notification.notification_type == 'connection_request':
        connection = ConnectionRequest.objects.filter(
            sender=notification.sender,
            reciver=notification.receiver
        ).first()
        if connection:
            return redirect('my-connections-requests')

        return redirect('my-notifications')
    
    if notification.notification_type == 'connection_accept':
        return redirect('profile',pk=notification.sender.profile.id)
    
    if notification.notification_type == 'comment':
        return redirect('post-detail',pk=notification.post.pk)
    
    if notification.notification_type == 'message':
        conversation = Conversation.objects.filter(participants=notification.receiver).filter(participants=notification.sender).first()
        if conversation:
            return redirect('conversation', pk=conversation.pk)

        return redirect('my-notifications')
    
    return redirect('my-notifications')