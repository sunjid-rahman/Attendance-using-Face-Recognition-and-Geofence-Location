from django.contrib import admin
from .models import UserProfile, Attendance, Geofence

admin.site.register(UserProfile)
admin.site.register(Attendance)
admin.site.register(Geofence)
