from django.core.management.base import BaseCommand
from courses.models import Course
import requests

class Command(BaseCommand):
    help = "Populate the database with course data from the PlanetTerp API"

    def handle(self, *args, **kwargs):
        url = "https://planetterp.com/api/v1/courses"
        limit = 100
        offset = 0
        total_courses = 0

        while True:
            params = {"limit": limit, "offset": offset}
            response = requests.get(url, params=params)

            if response.status_code != 200:
                self.stdout.write(self.style.ERROR("Failed to fetch data from API."))
                break

            data = response.json()
            if not data:  # Stop when there's no more data
                break
            
            created_count = 0
            updated_count = 0

            # Populate the Course model
            for course_data in data:
                print(f"Adding course: {course_data['name']}")
                obj, created = Course.objects.update_or_create(
                    name=course_data.get("name"),  # Lookup field
                    defaults={
                        "department": course_data.get("department"),
                        "course_number": course_data.get("course_number"),
                        "title": course_data.get("title"),
                        "description": course_data.get("description", ""),
                        "credits": course_data.get("credits", 0),
                        "average_gpa": course_data.get("average_gpa"),
                        "professors": course_data.get("professors", []),
                        "is_recent": True,
                        "name": course_data.get("name"),  # Populate the field
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1
                total_courses += 1

            offset += limit  # Fetch the next batch of results
        print(f"Total courses processed: {total_courses}")
        print(f"Courses created: {created_count}")
        print(f"Courses updated: {updated_count}")
        self.stdout.write(self.style.SUCCESS(f"Successfully populated {total_courses} courses."))
