from django.core.management.base import BaseCommand
from adverts.base.models import AdvertVisit


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        AdvertVisit.objects.create_from_cache()
        self.stdout.write(self.style.SUCCESS('Visits count has updated'))