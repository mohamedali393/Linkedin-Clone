from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import CompanyForm, JobForm, JobApplicationForm
from .models import Company, Job, JobApplication
from posts.forms import PostForm
from posts.models import Post
from notifications.models import Notification
from posts.forms import SharePostForm
from django.db.models import Q
from django.db.models import Sum

# Create your views here.


@login_required(login_url='login')
def index(request):
    form = PostForm()
    share_form = SharePostForm()
    posts = Post.objects.filter(
        Q(user=request.user) |
        Q(user__in=request.user.connections.all()) 
    )
    posts_views = Post.objects.filter(user=request.user).aggregate(total=Sum('views'))['total'] or 0

    context = {
        'form': form,
        'posts': posts,
        'share_form': share_form,
        'posts_views': posts_views,
    }
    return render(request,'jobs/index.html',context)


@login_required(login_url='login')
def jobs_page(request):
    jobs = Job.objects.all()

    context = {
        'jobs': jobs,
    }
    return render(request,'jobs/jobs.html',context)


@login_required(login_url='login')
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST,request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            messages.success(request,'Company Was created successfully')
            return redirect('my-companies')

    else:
        form = CompanyForm()

    context = {
        'form': form,
        'title': 'Create New Company'
    }
    return render(request,'create.html',context)



@login_required(login_url='login')
def my_companies(request):
    companies = Company.objects.filter(owner=request.user)

    context = {
        'companies': companies,
    }
    return render(request,'jobs/my-companies.html',context)


@login_required(login_url='login')
def company_details(request,pk):
    company = get_object_or_404(Company,pk=pk)

    context = {
        'company': company,
    }
    return render(request,'jobs/company-details.html',context)



@login_required(login_url='login')
def update_company(request,pk):
    company = get_object_or_404(Company,pk=pk)
    if company.owner != request.user:
        return HttpResponseForbidden('You don\'t Have permission to get access')
    
    if request.method == 'POST':
        form = CompanyForm(request.POST,request.FILES,instance=company)
        if form.is_valid():
            form.save()
            messages.success(request,'Company was updated successfully')
            return redirect('my-companies')
    else:
        form = CompanyForm(instance=company)

    context = {
        'form': form,
        'title': 'Update Company'
    }
    return render(request,'create.html',context)



@login_required(login_url='login')
def create_job(request,pk):
    company = get_object_or_404(Company,pk=pk)
    if company.owner != request.user:
        return HttpResponseForbidden('Your don\'t Have permission to get access')
    
    if request.method == 'POST':
        form = JobForm(request.POST,request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            # job.owner = request.user
            job.save()
            messages.success(request,'Job was created successfully')
            return redirect('my-companies')

    else:
        form = JobForm()

    context = {
        'form': form,
        'title': 'Create New Job'
    }
    return render(request,'create.html',context)


@login_required(login_url='login')
def post_new_job(request):
    companies = Company.objects.filter(owner=request.user)
    if len(companies) == 0:
        messages.error(request,'You must add a company before posting a new job')
        return redirect('jobs')
    
    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        title = request.POST.get('title')
        salary = request.POST.get('salary')
        experience_years = request.POST.get('experience_years')
        location = request.POST.get('location')
        description = ''
        if request.POST.get('description'):
            description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        job_type = request.POST.get('job_type')
        company = get_object_or_404(Company,pk=company_id)
        job = Job.objects.create(
            company=company,
            title=title,
            salary=salary,
            experience_years=experience_years,
            location=location,
            deadline=deadline,
            job_type=job_type,
            description=description
        )
        messages.success(request,'Job was posted successfully')
        return redirect('jobs')

    context = {
        'companies': companies,
    }
    return render(request,'jobs/create-new-job.html',context)



@login_required(login_url='login')
def delete_company(request,pk):
    company = get_object_or_404(Company,pk=pk)

    if company.owner != request.user:
        return HttpResponseForbidden('You don\'t Have permission to get access')
    
    if request.method == 'POST':
        company.delete()
        messages.success(request,'Company was deleted successfully')
        return redirect('my-companies')
    
    context = {
        'obj': company,
    }
    return render(request,'delete.html',context)



@login_required(login_url='login')
def applie_job(request,pk):
    job = get_object_or_404(Job,pk=pk)
    if job.company.owner == request.user:
        return HttpResponseForbidden('Your can\'t Applie your own job company')
    
    if JobApplication.objects.filter(job=job,user=request.user).exists():
        messages.error(request,'You already applied for that job')
        return redirect('jobs')
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST,request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.save()
            Notification.objects.create(
                sender=request.user,
                receiver=job.company.owner,
                job=job,
                message=f'{request.user.full_name} has applied to your job',
                notification_type='job_application'
            )
            messages.success(request,'You Successfully applied for that job')
            return redirect('jobs')
    else:
        form = JobApplicationForm()

    context = {
        'form': form,
        'title': f'{job.title} Application'
    }
    return render(request,'create.html',context)



@login_required(login_url='login')
def my_applications(request):
    applications = JobApplication.objects.filter(user=request.user)

    context = {
        'applications': applications,
    }
    return render(request,'jobs/my-applications.html',context)



@login_required(login_url='login')
def job_details(request,pk):
    job = get_object_or_404(Job,pk=pk)

    context = {
        'job': job,
    }
    return render(request,'jobs/job-details.html',context)



@login_required(login_url='login')
def job_applications(request,pk):
    job = get_object_or_404(Job,pk=pk)
    applications = JobApplication.objects.filter(job=job)

    context = {
        'job': job,
        'applications': applications,
    }
    return render(request,'jobs/job-applications.html',context)



@login_required(login_url='login')
def update_job(request,pk):
    job = get_object_or_404(Job,pk=pk)
    if job.company.owner != request.user:
        return HttpResponseForbidden('You don\'t have permission to get access')
    
    if request.method == 'POST':
        form = JobForm(request.POST,request.FILES,instance=job)
        if form.is_valid():
            form.save()
            messages.success(request,'Job Was Updated successfully')
            return redirect('job',pk=job.pk)
    else:
        form = JobForm(instance=job)

    context = {
        'form': form,
    }
    return render(request,'create.html',context)


@login_required(login_url='login')
def delete_job(request,pk):
    job = get_object_or_404(Job,pk=pk)
    if job.company.owner != request.user:
        return HttpResponseForbidden('You don\'t have permission to get access')
    if request.method == 'POST':
        job.delete()
        messages.success(request,'Job was deleted successfully')
        return redirect('job',pk=pk)
    
    context = {
        'obj': job
    }
    return render(request,'delete.html',context)



@login_required(login_url='login')
def accept_job_application(request,pk):
    job_application = get_object_or_404(JobApplication,pk=pk)
    if job_application.job.company.owner != request.user:
        return HttpResponseForbidden('You don\'t Have permission to perform this action')
    
    job_application.status = 'accepted'
    job_application.save()
    Notification.objects.create(
        sender=request.user,
        receiver=job_application.user,
        job=job_application.job,
        message=f'{request.user.full_name} has Accepted to your job Application',
        notification_type='job_application'
    )
    messages.success(request,'Job application was accepted successfully')
    return redirect('job',pk=job_application.job.pk)


@login_required(login_url='login')
def reject_job_application(request,pk):
    job_application = get_object_or_404(JobApplication,pk=pk)
    if job_application.job.company.owner != request.user:
        return HttpResponseForbidden('You don\'t have permission to get access')
    
    job_application.status = 'rejected'
    job_application.save()
    messages.success(request,'You Successfully rejected that job application')
    return redirect('job',pk=job_application.job.pk)