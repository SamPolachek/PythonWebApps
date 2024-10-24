from django.core.management.base import BaseCommand
from requests import get

class Command(BaseCommand):

    def handle(self, *args, **options):
        print('my command script')

get("https://shrinking-world.com")