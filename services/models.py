from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    REQUEST_TYPES = [
        ('LEAK', 'Gas Leak'),
        ('BILLING', 'Billing Issue'),
        ('MAINTENANCE', 'Maintenance Request'),
        ('OTHER', 'Other'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='service_requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    details = models.TextField()
    attachment = models.FileField(upload_to='uploads/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    submitted_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')

    def __str__(self):
        return f"{self.request_type} - {self.customer.user.username} - {self.status}"