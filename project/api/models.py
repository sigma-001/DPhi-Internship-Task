from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

SUBMISSION_TYPES = [
    ('file', 'file'),
    ('image', 'image'),
    ('url', 'url')
]

class Hackathon(models.Model):
    
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'created_hackathons')
    title = models.CharField(max_length = 255)
    description = models.TextField()
    background_image = models.ImageField(blank = True, null = True)
    hackathon_image = models.ImageField(blank = True, null = True)
    submission_type = models.CharField(max_length = 15,choices = SUBMISSION_TYPES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reward_prize = models.PositiveBigIntegerField()
    enrolled_by = models.ManyToManyField(User, related_name = 'enrolled_hackathons', blank = True)
    
    
    class Meta:
        constraints = [
            models.CheckConstraint(check = models.Q(end_time__gte= models.F('start_time')), 
                                   name = "correct end time",
                                   violation_error_message= "End time should be greater than starting time"),
        ]
        
    def __str__(self):
        return f"{self.title} --> {self.start_time}"
        
    
    
class HackathonSubmission(models.Model):
    
    submitted_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'hackathon_submissions')
    hackathon = models.ForeignKey(Hackathon, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    summary = models.TextField()
    description = models.TextField()
    file = models.FileField(blank = True, null = True)
    image = models.ImageField(blank = True, null = True)
    url = models.URLField(blank = True, null = True)
    starred_by = models.ManyToManyField(User, blank = True, related_name = "favourite_submissions")
    
    def __str__(self):
        return f"{self.hackathon.title} --> {self.title}"
    
    