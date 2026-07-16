from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from .models import Conversation, Message
from .forms import MessageForm
from django.contrib import messages
from django.db.models import Q
from notifications.models import Notification

# Create your views here.

@login_required(login_url='login')
def create_conversation(request,pk):
    if request.method == 'POST':
        reciver = get_object_or_404(Account,pk=pk)
        
        if reciver == request.user:
            return redirect('create-conversation')
        
        if not request.user in reciver.connections.all():
            messages.error(request,'You are\'t Connected together')
            return redirect('index')
        
        conversation = Conversation.objects.filter(participants=request.user).filter(participants=reciver).first()

        if not conversation:
            conversation = Conversation.objects.create()

            conversation.participants.add(reciver)
            conversation.participants.add(request.user)
            recivers = conversation.participants.all()
            for reciver in recivers:
                Notification.objects.create(
                    sender=request.user,
                    receiver=reciver,
                    message=f'{request.user.full_name} Send you a message',
                    notification_type='message'
                )
        return redirect('conversation',pk=conversation.id)
    
    return redirect('index')


@login_required(login_url='login')
def conversation_detail(request,pk):
    conversation = get_object_or_404(Conversation,pk=pk)
    contact_messages = Message.objects.filter(conversation=conversation)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            return redirect('conversation',pk=pk)
    else:
        form = MessageForm()
    context = {
        'conversation': conversation,
        'contact_messages': contact_messages,
        'form': form,
    }
    return render(request,'contact/conversation.html',context)


@login_required(login_url='login')
def messagings(request):
    conversations = Conversation.objects.filter(
        participants=request.user
    )
    
    context = {
        'conversations': conversations
    }
    return render(request,'contact/messagings.html',context)