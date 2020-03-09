from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    location = models.TextField()
    ticket_price = models.IntegerField()
    ticket_amount = models.IntegerField()
    picture = models.ImageField(upload_to='photos/', null=True)
    is_popular = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, through='event.Ticket')

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchased_date = models.DateField(auto_now=True)