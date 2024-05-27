from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Passenger, Schedule, Bus, Ticket

# Register your models here.
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Passenger)
admin.site.register(Schedule)
admin.site.register(Bus)
admin.site.register(Ticket)