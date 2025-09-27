from django.shortcuts import render
from django.http import JsonResponse
from courses.models import Course  # Import the Course model
from professors.models import Prof # Import the Prof model

def get_courses(request):
    # Fetch all courses from the database
    all_courses = list(Course.objects.values())
    print(len(all_courses))
    return JsonResponse(all_courses, safe=False)

def filter_courses(request, prof_name):
    try:
        prof = Prof.objects.get(name=prof_name)
        return JsonResponse({"courses": list(set(prof.courses))})
    except Prof.DoesNotExist:
         return JsonResponse({"error": "Professor not found"}, status=404)

# NEW view to render the HTML page
def course_search_page(request):
    return render(request, 'page.html')  # Path to your HTML template
