from django.core.management.base import BaseCommand
from webhook.models import RequestLog
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Delete RequestLog entries older than the specified number of days."

    def add_arguments(self, parser):
        parser.add_argument(
            'duration_in_days',
             type=int,
             metavar="DAYS",
             help="Delete logs older than this many days.",
        )

    def handle(self, *args, **options):
        try:
            cutoff = timezone.now() - timedelta(
                  days=options["duration_in_days"]
            )

            deleted, _ =RequestLog.objects.filter(
                 received_at__lte=cutoff
            ).delete()

        except Exception as exc:
            raise CommandError(f"Failed to clean up logs: {exc}")
            

        self.stdout.write(
            self.style.SUCCESS(f"Deleted {deleted} old logs.")
        )

