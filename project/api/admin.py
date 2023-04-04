from django.contrib import admin
from .models import Hackathon, HackathonSubmission


class HackathonAdmin(admin.ModelAdmin):
    list_display = ('id','creator','title','reward_prize', 'start_time')
    
class HackathonSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id','submitted_by','title','hackathon')

admin.site.register(Hackathon, HackathonAdmin)
admin.site.register(HackathonSubmission, HackathonSubmissionAdmin)

