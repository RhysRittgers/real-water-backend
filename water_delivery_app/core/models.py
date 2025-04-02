# The above code defines Django models for scheduling deliveries and tracking jug returns.
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import date, time 


FREQUENCY_CHOICES = [
    ('WEEKLY', 'weekly'),
    ('BIWEEKLY', 'Biweekly'),
    ('MONTHLY', 'monthly'),
]

STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('DELIVERED', 'Delivered'),
    ('SKIPPED', 'Skipped'),
    ('PAUSED', 'Paused'),
]

# Create your models here.
class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    event_date = models.DateField()
    next_delivery_date = models.DateField(null = True, blank = True)
    delivery_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    date_created = models.DateTimeField(auto_now_add=True)
    subscription = models.BooleanField(default=False)
    shopify_sub_id = models.CharField(max_length=100, blank=True, null=True)
    jugs_per_delivery = models.IntegerField(default=0)
    shopify_customer_id = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return(f"{self.user} - {self.delivery_status} - {self.frequency} - {self.event_date} - {self.date_created} - {self.subscription} - {self.next_delivery_date} - {self.jugs_per_delivery}")
    
    def as_dict(self, include_internal=False):
        data = {
            "user": self.user.username,
            "frequency": self.frequency,
            "next_delivery_date": self.next_delivery_date.strftime("%Y-%m-%d") if self.next_delivery_date else None,
            "jugs_per_delivery": self.jugs_per_delivery,
            "delivery_status": self.delivery_status,
            "subscription": self.subscription,
            "shopify_sub_id": self.shopify_sub_id,
            "shopify_customer_id": self.shopify_customer_id,
        }
        
        if include_internal:
            data["event_data"] = self.event_date.strftime("%Y-%m-%d")
        return data
        
    def is_active(self):
        return self.subscription and self.event_date >= timezone.now().date()
    
class JugReturn(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='jug_returns_entries')
    return_date = models.DateField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.schedule.user.username} returned {self.amount} jugs on {self.return_date}"