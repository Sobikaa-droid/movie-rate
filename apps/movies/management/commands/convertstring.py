from django.core.management import BaseCommand
from apps.movies.models import Movie


class Command(BaseCommand):
    def handle(self, *args, **options):
        qs = Movie.objects.all()

        for obj in qs:
            obj.runtime = str(obj.runtime)
            obj.save()

        self.stdout.write("Successfully converted type from INT to STR of the field RUNTIME", ending="")
