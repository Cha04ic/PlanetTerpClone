from django.contrib import admin
from django.urls import path, include
# from courses.views import course_search_page  # Import the view function

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviews.urls')),
    path('', include('courses.urls')),  # Include other course-related URLs
    path('', include('professors.urls')), # Include professors URLS
    path('', include('grades.urls')), # Include grades URLS
]
