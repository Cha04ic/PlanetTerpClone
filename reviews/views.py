from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Review
from courses.models import Course
from professors.models import Prof
from grades.models import Grade
from django.utils import timezone

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if User.objects.filter(username=username).exists():
            error_msg = 'Username already exists'
            return JsonResponse({'success': False, 'error': error_msg})

        try:
            print(f"Trying to register username: {username}")
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)  # ✅ now safely inside the try block
            return JsonResponse({'success': True, 'redirect_url': '/'})
        except IntegrityError:
            error_msg = 'Username already exists'
            if is_ajax:
                return JsonResponse({'success': False, 'error': error_msg})


def login_view(request):
   if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Username or password is incorrect'})

   return JsonResponse({'success': False, 'error': 'Invalid request'})

def add_review(request):
    if request.method == 'POST':
        course_code = request.POST.get('course')
        prof_name = request.POST.get('professor')
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        grade = request.POST.get('grade')
        anonymous = request.POST.get('anonymous')
        author = request.user 

        course = get_object_or_404(Course, name=course_code)
        professor = get_object_or_404(Prof, name=prof_name)

        try:
            review = Review(
                professor=professor,
                course=course,
                rating=rating,
                grade=grade,
                comment=comment,
                author=author,
                anonymous=True if anonymous == 'true' else False
            )
            review.save()
            return JsonResponse({
                'professor': professor.name,
                'course': course.name,
                'rating': review.rating,
                'grade': review.grade,
                'comment': review.comment,
                'author': review.author.username if not review.anonymous else "Anonymous",
                'date_posted': review.date_posted.strftime('%m/%d/%Y'),
            })
        except IntegrityError as e:
            return JsonResponse({'status': 'fail', 'error': str(e)}, status=500)

def load_reviews(request):
    filter = request.GET.get('filter')
    data = []
    if filter:
         print("yo")
         query = request.GET.get('query')
         isCourse = request.GET.get('is_course') == 'true'
         if isCourse:
            course = Course.objects.get(name=query)
            reviews = Review.objects.filter(course=course).order_by('-date_posted')
         else:
            professor = Prof.objects.get(name=query)
            reviews = Review.objects.filter(professor=professor).order_by('-date_posted')
         data = [{
                'professor': review.professor.name,
                'course': review.course.name,
                'rating': review.rating,
                'grade': review.grade,
                'comment': review.comment,
                'author': review.author.username if not review.anonymous else "Anonymous",
                'date_posted': review.date_posted.strftime("%Y-%m-%d"),
            } for review in reviews]
    else:
        author = request.user
        reviews = Review.objects.filter(author=author).order_by('-date_posted')
        data = [{
             'professor': review.professor.name,
                'course': review.course.name,
                'rating': review.rating,
                'grade': review.grade,
                'comment': review.comment,
                'author': review.author.username if not review.anonymous else "Anonymous",
                'anonymous': review.anonymous,
                'date_posted': review.date_posted.strftime("%Y-%m-%d"),
        } for review in reviews]
    return JsonResponse(data, safe=False)


def home(request):
    context = {'course_count': Course.objects.count(),
               'professor_count': Prof.objects.count(),
               'review_count': Review.objects.count(),
               'grade_count': Grade.objects.count()
              }
    return render(request, 'page.html', context)

