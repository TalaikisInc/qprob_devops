from django.core.management.base import BaseCommand, CommandError
from server.tasks import project_folders_helper


class Command(BaseCommand):
    help = "Cretes projects folders from a list."

    def handle(self, *args, **options):
        project_folders_helper()

        self.stdout.write(self.style.SUCCESS('Successfully created projects in database'))
