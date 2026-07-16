from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import date
from django.db.models import Q
# from dateutil.relativedelta import relativedelta

# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not first_name:
            raise ValueError('A user must have first_name')
        
        if not last_name:
            raise ValueError('A user must have last_name')
        
        if not username:
            raise ValueError('A user must have username')
        
        if not email:
            raise ValueError('A user must have email')
        
        if not password:
            raise ValueError('A user must have password')
        
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user
    

    def create_superuser(self,first_name,last_name,username,email,password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user

class Account(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    connections = models.ManyToManyField('self',blank=True,symmetrical=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','username']

    objects = AccountManager()
    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    

    def is_connected(self,user1):
        return user1 in self.connections.all()
    

class ConnectionRequest(models.Model):
    sender = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='sent_connection_requests')
    reciver = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='recived_connection_requests')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['sender','reciver']]

    def __str__(self):
        return f'{self.sender.full_name} - {self.reciver.full_name}'


class Profile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE,related_name='profile')
    location = models.CharField(max_length=100,blank=True)
    headline = models.CharField(max_length=255,blank=True)
    about = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profiles',default='profiles/user-default.png')
    cover_image = models.ImageField(upload_to='profiles',default='profiles/default.jpg')
    views = models.PositiveIntegerField(
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.full_name
    


class Skill(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class UserSkill(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.full_name} - {self.skill.name}'
    


class Education(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='educations')
    school_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError('Start Date should be less than end date')
        return super().clean()
    

    @property
    def period(self):
        num_days = (self.end_date - self.start_date).days
        years = int(num_days // 365)
        months = (num_days % 365) // 30
        return f"{years} years {months} months"

    def __str__(self):
        return f'{self.user.full_name} - {self.school_name}'
    


class Experience(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='experiences')
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True,blank=True)
    position = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    currently_working = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError('Start Date should be less than end date')
        return super().clean()
    
    @property
    def period(self):
        end = self.end_date or date.today()

        num_days = (end - self.start_date).days
        years = num_days // 365
        months = (num_days % 365) // 30

        return f"{years} years {months} months"

    def __str__(self):
        return f'{self.user.full_name} - {self.company_name}'
    


class Language(models.Model):
    name = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class UserLanguage(models.Model):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    NATIVE = "native"

    PROFICIENCY_CHOICES = [
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (ADVANCED, "Advanced"),
        (NATIVE, "Native"),
    ]
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    proficiency = models.CharField(
        max_length=20,
        choices=PROFICIENCY_CHOICES,
        default=BEGINNER
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "language")

    def __str__(self):
        return f'{self.user.full_name} - {self.language.name}'