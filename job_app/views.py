from django.shortcuts import render,redirect,HttpResponseRedirect

# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# from .forms import SignUpForm, JobPostForm, RecruiterProfileEditForm,JobSeekerProfileEditForm ,UserEditForm,JobApplicationForm,CandidateForm
from .forms import *
from .models import JobPost, RecruiterProfile,JobSeekerProfile,Candidate,JobApplication,User
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetConfirmView,PasswordResetView
from django.urls import reverse_lazy
from django.contrib import messages

# def navbar(request):
#     return render(request,'navbar.html')

# Home Page
def home(request):
    data=Candidate.objects.all()
    return render(request,'home.html',{'data':data})

@csrf_exempt
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_recruiter = form.cleaned_data['is_recruiter']
            user.save()
            login(request, user)

            if user.is_recruiter:
                recruiterprofile, created = RecruiterProfile.objects.get_or_create(user=user)
            else:
                jobseekerprofile, created = JobSeekerProfile.objects.get_or_create(user=user)
            # user=User.objects.create_user(username=username,email=email,password=password)
            # user.save()

            user_subject="Welcome to our platform!"
            user_message=f"Hi {user.username},\n\nThank you for registering!\n\nBest Regards,\nTeam"
            send_mail(user_subject,user_message,settings.EMAIL_HOST_USER,[user.email],fail_silently=False)

            admin_subject="New Registration"
            admin_message=f"New user registered:\n\nUsername:{user.username}\nEmail:{user.email}\nPassword:{user.password}"
            send_mail(admin_subject,admin_message,settings.EMAIL_HOST_USER,['nnavaneetha557@gmail.com'],fail_silently=False)
            
            return redirect('job_app:home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def create_recruiter_profile(request):
    return render(request, 'recruiterprofilecreate.html')


@login_required
def job_updates(request):
    jobs = JobPost.objects.all()
    return render(request, 'job_updates.html', {'jobs': jobs})


@login_required
def job_detail(request, job_id):
    job = JobPost.objects.get(id=job_id)
    return render(request, 'job_detail.html', {'job': job})


@login_required
def company_details(request, recruiter_id):
    company = RecruiterProfile.objects.get(user_id=recruiter_id)
    return render(request, 'company_details.html', {'company': company})

@login_required
def post_job(request):
    if not request.user.is_recruiter:
        return redirect('job_app:home')

    if request.method == "POST":
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, "Job posted successfully!") 
            return redirect('job_app:home')
        else:
            print("Form errors:", form.errors)  
            messages.error(request, "Form submission failed. Check your inputs.")
    else:
        form = JobPostForm()
    
    return render(request, 'postjob.html', {'form': form})



def custom_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('job_app:home') 
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')



@login_required
def profile(request):
    if request.user.is_recruiter:  
        profile, created = RecruiterProfile.objects.get_or_create(user=request.user)

        if request.method == "POST":
            profile.company_name = request.POST.get("company_name")
            profile.company_website = request.POST.get("company_website")
            profile.company_description = request.POST.get("company_description")
            profile.location = request.POST.get("location")
            profile.industry = request.POST.get("industry")
            profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('job_app:profile')  

        return render(request, 'recruiterprofile.html', {'profile': profile})
    
    else:  
        profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)

        if request.method == "POST":
            profile.resume = request.FILES.get("resume")
            profile.skills = request.POST.get("skills")
            profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('job_app:profile')

        
        applied_jobs = JobApplication.objects.filter(job_seeker=request.user)
        
        return render(request, 'jobseekerprofile.html', {'profile': profile, 'applied_jobs': applied_jobs})

@login_required
def edit_profile(request):
    user = request.user  

    if user.is_recruiter:
        profile, created = RecruiterProfile.objects.get_or_create(user=user)
        profile_form_class = RecruiterProfileEditForm
    else:
        profile, created = JobSeekerProfile.objects.get_or_create(user=user)
        profile_form_class = JobSeekerProfileEditForm

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = profile_form_class(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('job_app:profile')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = profile_form_class(instance=profile)

    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

def logout_view(request):
    logout(request) 
    return redirect('job_app:home')  

@login_required
def apply_job(request, job_id):
    job = JobPost.objects.get(id=job_id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_seeker = request.user
            application.job_post = job
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('job_app:profile')
    else:
        form = JobApplicationForm()
    
    return render(request, 'apply_job.html', {'form': form, 'job': job})

def insert(request):
    if request.method=='POST':
        form=CandidateForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('job_app:home')
        
    c1=CandidateForm()
    return render(request,'insert.html',{'forms':c1})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_done.txt'
    form_class=CustomPasswordResetForm

    def form_valid(self, form):
        form.save(
            request=self.request,
            use_https=self.request.is_secure(),
            email_template_name=self.email_template_name,
            subject_template_name=self.subject_template_name,
        )
        context = self.get_context_data(form=form)
        context['email_sent'] = True  
        return self.render_to_response(context)



# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'registration/password_reset_confirm.html'

#     def form_valid(self, form):
#         """
#         When the form is valid, save the new password and render
#         the same template with a success message.
#         """
#         form.save()
#         context = self.get_context_data(form=form)
#         context['reset_success'] = True  
#         return self.render_to_response(context)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url=reverse_lazy('job_app:login')
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your password has been reset successfully!")
        # return redirect('job_app:login') 
        return HttpResponseRedirect(self.success_url)
        