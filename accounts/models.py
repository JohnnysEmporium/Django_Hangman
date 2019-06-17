from django.db import models

class Event(models.Model):
    name = models.CharField('Name', max_length=120)
    win = models.IntegerField(default = 0)
    loss = models.IntegerField(default = 0)
    
    
    def __str__(self):
        return self.name