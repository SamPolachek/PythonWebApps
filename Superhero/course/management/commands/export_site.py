from django.core.management.base import BaseCommand
from course.website import export_course


class Command(BaseCommand):

    def handle(self, *args, **options):
        export_course()