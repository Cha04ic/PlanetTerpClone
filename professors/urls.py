from django.urls import path
from . import views

urlpatterns = [
    path('profs/', views.get_profs, name = 'get_profs'),
    path('filter_profs/<str:course_name>/', views.filter_profs, name='filter_profs'),
]