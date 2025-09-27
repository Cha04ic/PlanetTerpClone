from django.shortcuts import render
from django.http import JsonResponse
from grades.models import Grade

def get_grades(request):
    course = request.GET.get('course')
    professor = request.GET.get('professor')

    if not course and not professor:
         return JsonResponse({"error": "At least one of course or professor is required."}, status=400)
    
    filters = {}
    if course:
         filters['course'] = course
    if professor:
         filters['professor'] = professor

    filtered_grades = list(Grade.objects.filter(**filters).values())
    return JsonResponse(filtered_grades, safe=False)



