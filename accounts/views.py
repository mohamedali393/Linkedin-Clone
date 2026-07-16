from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, SkillForm, EducationForm, ExperienceForm
from .models import Skill, UserSkill, Education, Experience, Language, UserLanguage, Account, Profile, ConnectionRequest
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from notifications.models import Notification

# Create your views here.

def has_connection_request(u1,u2):
    if u1 == u2:
        return False
    
    return ConnectionRequest.objects.filter(Q(sender=u1,reciver=u2) | Q(sender=u2,reciver=u1)).exists()

def loginUser(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        if '@' in username_or_email:
            try:
                validate_email(username_or_email)
            except ValidationError:
                messages.error(request,'Please Enter a valid email or a valid username')
                return redirect('login')
            
            account = Account.objects.filter(email=username_or_email).first()
            if account:
                username = account.username

            else:
                username = None

        else:
            username = username_or_email
        if not Account.objects.filter(username=username).exists():
            messages.error(request,'Wrong username or password')
            return redirect('login')
        
        print(username)
        user = authenticate(request,username=username,password=password)
        print(user)
        if not user:
            messages.error(request,'Wrong username or password')
            return redirect('login')
        
        login(request,user)
        messages.success(request,'User Logged in successfully')
        return redirect(next) if next else redirect('index')

    return render(request,'accounts/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        passwordConfirm = request.POST.get('passwordConfirm')

        if Account.objects.filter(email=email).exists():
            messages.error(request,'That Email is registered')
            return redirect('register')
        
        if Account.objects.filter(username=username).exists():
            messages.error(request,'An Email with that username is already found')
            return redirect('register')
        
        if password != passwordConfirm:
            messages.error(request,'Passwords Don\'t Match')
            return redirect('register')
        
        user = Account.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password
        )

        messages.success(request,'Account was created successfully for that user')
        return redirect('login')
    
    return render(request,'accounts/register.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.success(request,'User logged Out Successfully')
    return redirect('login')


@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    skills = Skill.objects.filter(userskill__user__profile=profile)
    educations = Education.objects.filter(user=profile.user)
    experiences = Experience.objects.filter(user=profile.user)
    languages = Language.objects.filter(userlanguage__user=profile.user)
    profiles = Profile.objects.order_by('-created_at')[:5]
    for p in profiles:
        p.is_connected = p.user.is_connected(request.user)
        p.has_connection_request = has_connection_request(request.user,p.user)
    context = {
        'profile': profile,
        'skills': skills,
        'educations': educations,
        'experiences': experiences,
        'languages': languages,
        'profiles': profiles,
    }
    return render(request,'accounts/user-account.html',context)



@login_required(login_url='login')
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Your Profile was updated successfully')
            return redirect('account')
        
    else:
        form = ProfileForm(instance=request.user.profile)

    context = {
        'form': form,
        'title': 'Update Your Profile'
    }
    return render(request,'create.html',context)



@login_required(login_url='login')
def create_skill(request):
    if request.method == 'POST':
        skill_name = request.POST.get('name').lower()
        skill, created = Skill.objects.get_or_create(name=skill_name)
        if UserSkill.objects.filter(skill=skill,user=request.user).exists():
            messages.error(request,'That skill is already exists')
            return redirect('account')
    
        u_skill = UserSkill.objects.create(
            skill=skill,
            user=request.user
        )
        messages.success(request, 'User skill was addess successfully')
        return redirect('account')
    
    context = {
        'title': 'Create New Skill'
    }
    return render(request,'accounts/create-skill.html',context)



@login_required(login_url='login')
def create_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            messages.success(request,'Education was added successfully')
            return redirect('account')

    else:
        form = EducationForm()

    context = {
        'form': form,
        'title': 'Add Education',
    }
    return render(request,'create.html',context)



@login_required(login_url='login')
def create_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            messages.success(request,'Experience was added successfully')
            return redirect('account')

    else:
        form = ExperienceForm()

    context = {
        'form': form,
        'title': 'Add Experience',
    }
    return render(request,'create.html',context)



@login_required(login_url='login')
def create_language(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        proficiency = request.POST.get('proficiency')
        language, created = Language.objects.get_or_create(name=name)
        if UserLanguage.objects.filter(language=language,user=request.user).exists():
            messages.error(request,'Language already found')
            return redirect('account')
        
        user_language = UserLanguage.objects.create(
            user=request.user,
            language=language,
            proficiency=proficiency
        )
        messages.success(request,'Language Was created Successfully')
        return redirect('account')
    
    return render(request,'accounts/create-language.html')


def profile_details(request,pk):
    profile = get_object_or_404(Profile,pk=pk)
    profile.views += 1
    profile.save()
    skills = Skill.objects.filter(userskill__user__profile=profile)
    educations = Education.objects.filter(user=profile.user)
    experiences = Experience.objects.filter(user=profile.user)
    languages = Language.objects.filter(userlanguage__user=profile.user)
    profile.is_connected = profile.user.is_connected(request.user)
    profile.has_connection_request = has_connection_request(profile.user,request.user)
    profiles = Profile.objects.order_by('-created_at')[:5]
    for p in profiles:
        p.is_connected = p.user.is_connected(request.user)
        p.has_connection_request = has_connection_request(request.user,p.user)

    context = {
        'profile': profile,
        'profiles': profiles,
        'skills': skills,
        'educations': educations,
        'experiences': experiences,
        'languages': languages,
    }
    return render(request,'accounts/user-account.html',context)



@login_required(login_url='login')
def create_connection(request,reciver_id):
    next = request.GET.get('next')
    reciver = get_object_or_404(Account,pk=reciver_id)
    if reciver == request.user:
        return redirect(next or 'index')
    
    if ConnectionRequest.objects.filter(Q(sender=request.user,reciver=reciver) | Q(sender=reciver,reciver=request.user)).exists():
        messages.error(request,'Connection is already exists')
        return redirect(next) if next else redirect('index')
    
    connection = ConnectionRequest.objects.create(
        sender=request.user,
        reciver=reciver
    )
    Notification.objects.create(
        sender=request.user,
        receiver=reciver,
        message=f'{request.user.full_name} Required your connection',
        notification_type='connection_request'
    )
    messages.success(request,'Your connection was created successfully')
    return redirect(next) if next else redirect('index')


@login_required(login_url='login')
def my_connections_requests(request):
    connections_requests = ConnectionRequest.objects.filter(reciver=request.user)
    
    context = {
        'requests': connections_requests,
    }
    return render(request,'accounts/my-connections-request.html',context)



@login_required(login_url='login')
def accept_user_connection(request,pk):
    if request.method == 'POST':
        connection_request = get_object_or_404(ConnectionRequest,reciver=request.user,pk=pk)
        next = request.POST.get('next')
        request.user.connections.add(connection_request.sender)
        connection_request.delete()
        Notification.objects.create(
            sender=request.user,
            receiver=connection_request.sender if request.user == connection_request.reciver else connection_request.reciver,
            message=f'{request.user.full_name} Required your connection',
            notification_type='connection_request'
        )
        messages.success(request,'Connection was created successfully')
        return redirect(next or 'index')
    
    return redirect('index')



@login_required(login_url='login')
def reject_user_connection(request,pk):
    if request.method == 'POST':
        connection_request = get_object_or_404(ConnectionRequest,reciver=request.user,pk=pk)
        next = request.POST.get('next')
        connection_request.delete()
        Notification.objects.create(
            sender=request.user,
            receiver=connection_request.sender if request.user == connection_request.reciver else connection_request.reciver,
            message=f'{request.user.full_name} Rejected your connection',
            notification_type='connection_reject'
        )
        messages.success(request,'Connection was rejected successfully')
        return redirect(next or 'index')
    
    return redirect('index')



@login_required(login_url='login')
def delete_connection(request,pk):
    if request.method == 'POST':
        user1 = get_object_or_404(Account,pk=pk)
        if user1 == request.user:
            return redirect('index')
        
        if user1 in request.user.connections.all():
            request.user.connections.remove(user1)
            messages.success(request,'Connection was removed successfully')
            return redirect('profile',pk=user1.profile.id)
        
        else:
            messages.error(request,'The is no connections between users')
            return redirect('profile',pk=user1.profile.id)
    
    return redirect('index')