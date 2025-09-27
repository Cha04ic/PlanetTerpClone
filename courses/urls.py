from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.get_courses, name='get_courses'),
    path('filter_courses/<str:prof_name>/', views.filter_courses, name='filter_courses'),
]
