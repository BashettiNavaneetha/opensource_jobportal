from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

User = get_user_model()



class SignUpForm(UserCreationForm):
    is_recruiter = forms.BooleanField(required=False, initial=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_recruiter')

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'responsibilities', 'requirements','skills','qualification', 'location', 'salary','experience_level', 'experience_range', 'apply_link']


class RecruiterProfileEditForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['company_name', 'location', 'industry', 'company_website', 'company_description']


class JobSeekerProfileEditForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['resume', 'skills']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['first_name', 'last_name', 'email', 'phone', 'resume', 'skills', 'cover_letter']

class CandidateForm(forms.ModelForm):
    class Meta:
        model=Candidate
        fields='__all__'

class CustomPasswordResetForm(PasswordResetForm):
    

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email address")
        return email            
    
