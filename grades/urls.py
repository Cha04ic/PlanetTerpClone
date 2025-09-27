from django.urls import path
from . import views

urlpatterns = [
    path('grades/', views.get_grades, name='get_grades'),
]