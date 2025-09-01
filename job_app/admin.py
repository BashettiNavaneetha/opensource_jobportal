from django.contrib import admin

# Register your models here.
from .models import Candidate

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile_pic')

admin.site.register(Candidate,CandidateAdmin)