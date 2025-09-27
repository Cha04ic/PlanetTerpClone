from django.core.management.base import BaseCommand
from professors.models import Prof
import requests

class Command(BaseCommand):
    help = "Populate the database with professor data"

    def handle(self, *args, **kwargs):
        url = "https://planetterp.com/api/v1/professors"
        limit = 100
        offset = 0
        total_profs = 0

        while True:
            params = {"limit": limit, "offset": offset}
            response = requests.get(url, params)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR("Failed to fetch data from API."))
                break
            data = response.json()
            if not data:
                break
            for prof_data in data:
                Prof.objects.update_or_create(
                    name = prof_data.get('name'),
                    defaults = {
                        "slug": prof_data.get('slug'),
                        "type": prof_data.get('type'),
                        "courses": prof_data.get('courses'),
                        "avg_rating": prof_data.get('average_rating')
                    }
                )
                total_profs += 1
            offset += limit
        self.stdout.write(self.style.SUCCESS(f"Successfully populated {total_profs} professors."))

