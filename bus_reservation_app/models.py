from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Custom User Model
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, "admin"),
        (2, "student"),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    student_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    year_of_study = models.PositiveIntegerField(null=True, blank=True)

# Admin Model
class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Student Model
class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255, null=True)
    college = models.CharField(max_length=255, null=True)
    year_of_study = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Bus Route Model
class BusRoute(models.Model):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    distance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['origin', 'destination']
    
    def __str__(self):
        return f"{self.origin} to {self.destination}"

# Bus Model
class Bus(models.Model):
    bus_number = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['bus_number']
    
    def __str__(self):
        return self.bus_number

# Stop Model
class Stop(models.Model):
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='stops')
    name = models.CharField(max_length=100)
    sequence_number = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('route', 'sequence_number')
        ordering = ['sequence_number']
    
    def __str__(self):
        return self.name

# Schedule Model
class Schedule(models.Model):
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='schedules')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='schedules')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    reservation_start_time = models.DateTimeField(null=True, blank=True)
    reservation_end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['departure_time']
    
    def is_within_reservation_period(self):
        now = timezone.now()
        return self.reservation_start_time <= now <= self.reservation_end_time

# Payment Model
class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['payment_date']

# Ticket Model
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='tickets')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='tickets')
    seat_number = models.CharField(max_length=10)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, related_name='tickets')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_reference = models.CharField(max_length=100, null=True, blank=True) 
    
    class Meta:
        unique_together = ('schedule', 'seat_number')
        ordering = ['booking_date']

# Signals for creating and saving profiles
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        elif instance.user_type == 2:
            Student.objects.create(admin=instance, address="")

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    elif instance.user_type == 2:
        instance.student.save()
