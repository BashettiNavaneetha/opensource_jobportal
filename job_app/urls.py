from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from .forms import CustomPasswordResetForm

app_name='job_app'
urlpatterns = [
    # path('',navbar,name='navbar'),
    path('', home, name='home'),
    path('signup/',signup, name='signup'),
    path('job_updates/',job_updates, name='job_updates'),
    path('job/<int:job_id>/',job_detail, name='job_detail'),
    path('company/<int:recruiter_id>/',company_details, name='company_details'),
    path('post_job/',post_job, name='post_job'),
    path('profile/',profile,name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('logout/',logout_view,name='logout'),
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('insert/',insert,name='insert'),
    
    path(
        'reset/<uidb64>/<token>/',
        CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),name='password_reset_complete'
    ),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]

