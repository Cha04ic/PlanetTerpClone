from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from professors.models import Prof
from courses.models import Course

def get_profs(request):
    all_profs = list(Prof.objects.values())
    print(len(all_profs))
    return JsonResponse(all_profs, safe=False)

def filter_profs(request, course_name):
    try:
        courses = Course.objects.get(name=course_name)
        return JsonResponse({"profs": list(set(courses.professors))})
    except Course.DoesNotExist: 
        return JsonResponse({"error": "Course not found"}, status=404)





