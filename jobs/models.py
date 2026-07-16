from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from accounts.models import Account
from django.urls import reverse

# Create your models here.

class Company(models.Model):
    owner = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='companies')
    name = models.CharField(max_length=100,unique=True)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='companies',default='companies/default.jpg')
    website = models.URLField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_url(self):
        return reverse('company-details',args=[self.id])

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    


class Job(models.Model):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"

    JOB_TYPES = [
        (FULL_TIME, "Full Time"),
        (PART_TIME, "Part Time"),
        (CONTRACT, "Contract"),
        (INTERNSHIP, "Internship"),
        (FREELANCE, "Freelance"),
    ]
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='jobs')
    salary = models.PositiveIntegerField()
    experience_years = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    deadline = models.DateField()
    description = models.TextField(blank=True)
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPES,
        default=FULL_TIME
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return self.title
    

def validate_file_size(file):
        max_size = 5 * 1024 * 1024  # 5 MB

        if file.size > max_size:
            raise ValidationError("Resume size cannot exceed 5 MB.")


class JobApplication(models.Model):
    PENDING = 'pending'
    REVIEWING = 'reviewing'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (REVIEWING, 'Reviewing'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='job_applications')
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name='applications')
    resume = models.FileField(upload_to='resumes',validators=[FileExtensionValidator(allowed_extensions=['pdf','doc', 'docx']),validate_file_size])
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.full_name} - {self.job.title}'