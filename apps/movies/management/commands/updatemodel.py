from django.core.management import BaseCommand
from apps.movies.models import MovieReview
from django.utils.text import slugify


class Command(BaseCommand):
    def handle(self, *args, **options):
        MovieReview.objects.filter(memo__isnull=True).delete()

        """ for obj in qs:
            obj.slug = slugify(str(obj.title))
            obj.save() """

        self.stdout.write("Successfully updated slugs on all objects", ending="")
