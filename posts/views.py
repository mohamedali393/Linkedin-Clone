from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse
from .forms import PostForm, CommentForm, SharePostForm
from .models import Post, Comment
from accounts.models import Profile, Account
from jobs.models import Job, Company
from django.db.models import Q
from notifications.models import Notification
from django.contrib.auth.decorators import login_required

# Create your views here.

class CreatePostView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request,'Post was created successfully')
            return redirect('index')
        
        return redirect('index')
    


def post_details(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.views += 1
    post.save(update_fields=['views'])
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            Notification.objects.create(
                sender=request.user,
                receiver=post.user,
                post=post,
                message=f'{request.user.full_name} Commented your post',
                notification_type='comment'
            )
            messages.success(request,'Comment was created successfully')
            return redirect(post.get_url)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request,'posts/post-details.html',context)


class UpdatePostView(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = 'create.html'
    fields = ['content']
    
    def get_success_url(self):
        post = self.get_object()
        return post.get_url
    

class UpdateCommentView(LoginRequiredMixin,UpdateView):
    model = Comment
    template_name = 'create.html'
    fields = ['content']

    def get_success_url(self):
        comment = self.get_object()
        return comment.post.get_url
    

class DeleteCommentView(LoginRequiredMixin,DeleteView):
    model = Comment
    template_name = 'delete.html'

    def get_success_url(self):
        return self.get_object().post.get_url
    



class LikePost(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post = get_object_or_404(Post,pk=pk)
        next = request.POST.get('next')

        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like :
            post.likes.remove(request.user)

        else:
            post.likes.add(request.user)
            Notification.objects.create(
                sender=request.user,
                receiver=post.user,
                post=post,
                message=f'{request.user.full_name} Liked your post',
                notification_type='like'
            )

        return redirect(next)
    


@login_required(login_url='login')
def search(request):
    q = request.GET.get('q')
    users = []
    posts = []
    jobs = []
    companies = []

    if q:
        users = Account.objects.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(username__icontains=q)
        )

        jobs = Job.objects.filter(
            Q(title__icontains=q) |
            Q(salary__icontains=q) |
            Q(description__icontains=q)
        )

        posts = Post.objects.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(user__username__icontains=q) |
            Q(content__icontains=q)
        )

        companies = Company.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    context = {
        'users': users,
        'posts': posts,
        'jobs': jobs,
        'companies': companies
    }
    return render(request,'posts/search.html',context)


@login_required(login_url='login')
def replay_comment(request,pk):
    if request.method == 'POST':
        parent = get_object_or_404(Comment,pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.parent = parent
            comment.user = request.user
            comment.post = parent.post
            comment.save()
            messages.success(request,'Successfully replayed comment')
            return redirect('post-detail',pk=parent.post.pk)
        
        return redirect('post-detail',pk=parent.post.pk)
    



@login_required(login_url='login')
def share_post(request,pk):
    if request.method == 'POST':
        post = get_object_or_404(Post,pk=pk)
        form = SharePostForm(request.POST)
        if form.is_valid():
            shared_body = form.cleaned_data['shared_body']
            shared_post = Post.objects.create(
                shared_post=post,
                shared_by=request.user,
                shared_body=shared_body,
                user=post.user
            )
            messages.success(request,'Successfully Shared Post')
            return redirect('index')
        
        return redirect('index')
    
    return redirect('index')