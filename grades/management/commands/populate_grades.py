from django.core.management.base import BaseCommand
from grades.models import Grade
from courses.models import Course
from professors.models import Prof
import requests

class Command(BaseCommand):
    help = "Populate the database with grades"

    def handle(self, *args, **kwargs):
       url = "https://planetterp.com/api/v1/grades"
       # loop through all courses & professors
       courses = Course.objects.values_list('name', flat=True)
       professors = Prof.objects.values_list('name', flat=True)

       # Fetch grades for courses only
       for course in courses:
           self.fetch_and_save_grades(url, {"course": course})
       # Fetch grades for professor only
       for professor in professors:
           self.fetch_and_save_grades(url, {"professor": professor})
       # Fetch grades for both courses & professors
       for course in courses:
           for professor in professors:
               self.fetch_and_save_grades(url, {"course": course, "professor": professor})

    def fetch_and_save_grades(self, url, params):
        response = requests.get(url, params)
        if response.status_code == 200:
            grades_data = response.json()
            for grade in grades_data:
                Grade.objects.update_or_create(
                    course = grade.get('course'),
                    semester = grade.get('semester'),
                    section = grade.get('section'),
                    defaults = {
                        "professor": grade.get('professor'),
                        "a_plus": grade.get('A+'),
                        "a": grade.get('A'),
                        "a_minus": grade.get('A-'),
                        "b_plus": grade.get('B+'),
                        "b": grade.get('B'),
                        "b_minus": grade.get('B-'),
                        "c_plus": grade.get('C+'),
                        "c": grade.get('C'),
                        "c_minus": grade.get('C-'),
                        "d_plus": grade.get('D+'),
                        "d": grade.get('D'),
                        "d_minus": grade.get('D-'),
                        "f": grade.get('F'),
                        "w": grade.get('W'),
                        "other": grade.get('Other')
                    }
                )
            self.stdout.write(self.style.SUCCESS(f"Successfully saved grades for {params}"))
        else:
             self.stdout.write(self.style.ERROR(f"Failed to fetch grades for {params}"))
