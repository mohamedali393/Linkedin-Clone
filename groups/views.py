from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import GroupForm, GroupPostForm, GroupCommentForm
from .models import Group, GroupRequest, GroupPost, GroupComment

# Create your views here.

@login_required(login_url='login')
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST,request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()
            messages.success(request,'Group was created successfully')
            return redirect('groups')
    else:
        form = GroupForm()

    context = {
        'form': form,
        'title': 'Create Group'
    }
    return render(request,'create.html',context)


@login_required(login_url='login')
def groups(request):
    groups = Group.objects.all()

    context = {
        'groups': groups,
    }
    return render(request,'groups/groups.html',context)



@login_required(login_url='login')
def group_detail(request,pk):
    group = get_object_or_404(Group,pk=pk)
    if group.is_private:
        if not (group.owner == request.user or request.user in group.members.all()):
            return HttpResponseForbidden('You don\'t Have permission to get access')
    if request.method == 'POST':
        form = GroupPostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.group = group
            post.user = request.user
            post.save()
            messages.success(request,'Post was sent to group successfully')
            return redirect('group-detail',pk=pk)
    else:
        form = GroupPostForm() 

    context = {
        'group': group,
        'form': form,
    }
    return render(request,'groups/group-detail.html',context)



@login_required(login_url='login')
def join_group(request,pk):
    group = get_object_or_404(Group,pk=pk)
    if group.owner == request.user:
        messages.error(request, "You are already the owner of this group")
        return redirect('groups')
    
    if request.user in group.members.all():
        messages.error(request,'You have aleady joined')
        return redirect('groups')
    
    if group.is_private:
        if GroupRequest.objects.filter(user=request.user,group=group).exists():
            messages.error(request,'You already sent a request for joining that group')
            return redirect('groups')
        GroupRequest.objects.create(
            group=group,
            user=request.user
        )
        messages.success(request,'Join Group request was sent successfully')
        return redirect('groups')
    
    group.members.add(request.user)
    messages.success(request,'You successfully Joied that group')
    return redirect('groups')



@login_required(login_url='login')
def accept_group_request(request,pk):
    group_request = get_object_or_404(GroupRequest,pk=pk)
    group = group_request.group
    if group.owner != request.user:
        return HttpResponseForbidden('You don\'t have permission to get access')

    group.members.add(group_request.user)
    group_request.delete()
    messages.success(request,'User was added to group successfully')
    return redirect('group-detail',pk=group.pk)



@login_required(login_url='login')
def reject_group_request(request,pk):
    group_request = get_object_or_404(GroupRequest,pk=pk)
    group = group_request.group
    if group.owner != request.user:
        return HttpResponseForbidden('You don\'t have permission to get access')

    group_request.delete()
    messages.success(request,'Join Group Request was rejected successfully')
    return redirect('group-detail',pk=group.pk)


@login_required(login_url='login')
def leave_group(request,pk):
    if request.method == 'POST':
        group = get_object_or_404(Group,pk=pk)
        if request.user == group.owner:
            messages.error(request,'You Can\'t Leave your own group')
            return redirect('group-detail',pk=pk)
        
        if request.user in group.members.all():
            group.members.remove(request.user)
            messages.success(request,'You successfully leaved that group')
            return redirect('index')
        
        return redirect('index')
    
    return redirect('index')



@login_required(login_url='login')
def like_post_group(request,pk):
    group_post = get_object_or_404(GroupPost,pk=pk)
    is_like = False
    for like in group_post.likes.all():
        if like == request.user:
            is_like = True
            break

    if not is_like:
        group_post.likes.add(request.user)

    else:
        group_post.likes.remove(request.user)

    return redirect('group-detail',pk=group_post.group.pk)


@login_required(login_url='login')
def group_post_detail(request,pk):
    group_post = get_object_or_404(GroupPost,pk=pk)
    comments = GroupComment.objects.filter(post=group_post)

    if not (group_post.group.owner == request.user or request.user in group_post.group.members.all()):
        return HttpResponseForbidden('You don\'t have permission to get access')
    
    if request.method == 'POST':
        form = GroupCommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = group_post
            comment.user = request.user
            comment.save()
            messages.success(request,'Comment was added successfully')
            return redirect('group-post-detail',pk=pk)
    else:
        form = GroupCommentForm()
    context = {
        'post': group_post,
        'comments': comments,
        'form': form
    }
    return render(request,'groups/group-post-detail.html',context)