from django.core.management import BaseCommand
from apps.movies.models import MovieReview
from apps.users.models import UserActivity
from django.utils.text import slugify


class Command(BaseCommand):
    def handle(self, *args, **options):
        UserActivity.objects.all().delete()

        """ for obj in qs:
            obj.slug = slugify(str(obj.title))
            obj.save() """

        self.stdout.write("Success!", ending="")
