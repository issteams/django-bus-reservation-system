from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Student, Schedule, Bus, Ticket

# Register your models here.
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Student)
admin.site.register(Schedule)
admin.site.register(Bus)
admin.site.register(Ticket)