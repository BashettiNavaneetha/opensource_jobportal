from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.contrib.auth import get_user_model
# from .models import User 
from django.conf import settings 

# Custom User Model
class User(AbstractUser):
    is_recruiter = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set", blank=True)

# Job Seeker Profile
class JobSeekerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    skills = models.TextField()
    
    def __str__(self):
        return self.user.username

# Recruiter Profile
class RecruiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_website = models.URLField()
    company_description = models.TextField()
    location = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    
    def __str__(self):
        return self.company_name



class JobPost(models.Model):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_recruiter': True})
    title = models.CharField(max_length=255)
    description = models.TextField()
    responsibilities = models.TextField(null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    skills=models.TextField(null=True, blank=True)
    qualification=models.CharField(max_length=100,null=True, blank=True)
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True)
    EXPERIENCE_CHOICES = [
        ('Fresher', 'Fresher'),
        ('Experienced', 'Experienced'),
    ]
    experience_level = models.CharField(max_length=15, choices=EXPERIENCE_CHOICES, default='Fresher')
    experience_range = models.CharField(max_length=100, blank=True, null=True)
    apply_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title



class JobApplication(models.Model):
    job_seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_recruiter': False})
    job_post = models.ForeignKey('JobPost', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    skills = models.TextField()
    cover_letter = models.TextField()
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_post.title}"
    
class Candidate(models.Model):
    name = models.CharField(max_length=50)
    company_name=models.CharField(max_length=100,default="Unknown Company")
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.name