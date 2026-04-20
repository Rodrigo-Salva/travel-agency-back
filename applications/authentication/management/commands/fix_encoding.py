"""
Fix double-encoded UTF-8 strings in database.
Run: python manage.py fix_encoding
"""
from django.core.management.base import BaseCommand
from applications.authentication.models import User
from applications.destinations.models import Destination
from applications.hotels.models import Hotel
from applications.activities.models import Activity
from applications.packages.models import Package, Category
from applications.flights.models import Flight
from applications.inquiries.models import Inquiry


def fix(text: str) -> str:
    """Repair text that was double-encoded (latin-1 decoded as utf-8)."""
    if not text:
        return text
    try:
        repaired = text.encode('latin-1').decode('utf-8')
        # Only return repaired if it actually changed and looks better
        return repaired
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def fix_obj(obj, fields: list[str]) -> bool:
    changed = False
    for field in fields:
        original = getattr(obj, field, '') or ''
        repaired = fix(original)
        if repaired != original:
            setattr(obj, field, repaired)
            changed = True
    return changed


class Command(BaseCommand):
    help = 'Fix double-encoded UTF-8 strings across all app models'

    def handle(self, *args, **options):
        total = 0

        # Users
        for obj in User.objects.all():
            if fix_obj(obj, ['first_name', 'last_name', 'country', 'city', 'address', 'nationality']):
                obj.save(update_fields=['first_name', 'last_name', 'country', 'city', 'address', 'nationality'])
                total += 1
                self.stdout.write(f'  User fixed: {obj.username}')

        # Destinations
        for obj in Destination.objects.all():
            if fix_obj(obj, ['name', 'country', 'description', 'short_description', 'best_season']):
                obj.save(update_fields=['name', 'country', 'description', 'short_description', 'best_season'])
                total += 1
                self.stdout.write(f'  Destination fixed: {obj.name}')

        # Hotels
        for obj in Hotel.objects.all():
            if fix_obj(obj, ['name', 'address', 'description', 'amenities']):
                obj.save(update_fields=['name', 'address', 'description', 'amenities'])
                total += 1
                self.stdout.write(f'  Hotel fixed: {obj.name}')

        # Activities
        for obj in Activity.objects.all():
            if fix_obj(obj, ['name', 'description']):
                obj.save(update_fields=['name', 'description'])
                total += 1
                self.stdout.write(f'  Activity fixed: {obj.name}')

        # Packages
        for obj in Package.objects.all():
            if fix_obj(obj, ['name', 'description', 'short_description']):
                obj.save(update_fields=['name', 'description', 'short_description'])
                total += 1
                self.stdout.write(f'  Package fixed: {obj.name}')

        # Categories
        for obj in Category.objects.all():
            if fix_obj(obj, ['name', 'description']):
                obj.save(update_fields=['name', 'description'])
                total += 1
                self.stdout.write(f'  Category fixed: {obj.name}')

        # Flights
        for obj in Flight.objects.all():
            if fix_obj(obj, ['airline_name', 'origin_city', 'destination_city', 'origin_airport', 'destination_airport']):
                obj.save(update_fields=['airline_name', 'origin_city', 'destination_city', 'origin_airport', 'destination_airport'])
                total += 1
                self.stdout.write(f'  Flight fixed: {obj.airline_name}')

        # Inquiries
        for obj in Inquiry.objects.all():
            if fix_obj(obj, ['name', 'subject', 'message', 'admin_response']):
                obj.save(update_fields=['name', 'subject', 'message', 'admin_response'])
                total += 1
                self.stdout.write(f'  Inquiry fixed: {obj.subject}')

        self.stdout.write(self.style.SUCCESS(f'\nDone. {total} records fixed.'))
