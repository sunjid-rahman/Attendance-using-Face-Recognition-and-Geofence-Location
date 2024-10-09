
from django.contrib import admin
from django.urls import path
from attendance.views import AttendanceView

urlpatterns = [
    path('attendance', AttendanceView.as_view(),name='attendance'),
]
