import django
from django.db import models

# Create your models here.
class Note(models.Model):
    text = models.TextField()
    date = models.DateField(default=django.utils.timezone.now)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()
        
    def __str__(self):
        return self.text