"""
Fix corrupted text data by directly updating known records.
Run: python manage.py fix_data
"""
from django.core.management.base import BaseCommand
from applications.authentication.models import User
from applications.destinations.models import Destination
from applications.activities.models import Activity
from applications.packages.models import Package, Category
from applications.flights.models import Flight
from applications.inquiries.models import Inquiry


class Command(BaseCommand):
    help = 'Fix corrupted text in known records'

    def handle(self, *args, **options):
        # Users
        User.objects.filter(username='maria.garcia').update(first_name='María', last_name='García')
        User.objects.filter(username='pedro.lopez').update(first_name='Pedro', last_name='López')
        User.objects.filter(username='ana.martinez').update(first_name='Ana', last_name='Martínez')
        User.objects.filter(username='juan.perez').update(first_name='Juan', last_name='Pérez')
        self.stdout.write('  Users fixed')

        # Destinations
        Destination.objects.filter(id=6).update(name='Cancún', country='México')
        self.stdout.write('  Destinations fixed')

        # Activities
        Activity.objects.filter(id=2).update(name='Camino Inca 4 días')
        Activity.objects.filter(id=6).update(name='Cañón del Colca 2 días')
        Activity.objects.filter(id=8).update(name='Expedición Amazonas')
        Activity.objects.filter(id=5).update(name='Sobrevuelo Líneas de Nazca')
        self.stdout.write('  Activities fixed')

        # Packages
        Package.objects.filter(id=1).update(name='Cusco Mágico y Machu Picchu')
        Package.objects.filter(id=3).update(name='Arequipa Colonial y Cañón del Colca')
        Package.objects.filter(id=4).update(name='Lago Titicaca Místico')
        Package.objects.filter(id=5).update(name='Aventura Amazónica en Iquitos')
        Package.objects.filter(id=6).update(name='Cancún Todo Incluido')
        Package.objects.filter(id=8).update(name='Cartagena Romántica')
        self.stdout.write('  Packages fixed')

        # Categories
        Category.objects.filter(id=7).update(name='Romántico')
        Category.objects.filter(id=8).update(name='Gastronómico')
        self.stdout.write('  Categories fixed')

        # Flights
        Flight.objects.filter(id=6).update(airline_name='Aeroméxico')
        Flight.objects.filter(id=8).update(airline_name='Aerolíneas Argentinas')
        self.stdout.write('  Flights fixed')

        # Inquiries
        Inquiry.objects.filter(name__contains='Luc').update(name='Lucía Fernández')
        Inquiry.objects.filter(subject__contains='Cotizaci').update(subject='Cotización para grupo corporativo')
        Inquiry.objects.filter(name__contains='Guti').update(name='Patricia Gutiérrez')
        Inquiry.objects.filter(subject__icontains='paquetes incluyen').update(subject='¿Los paquetes incluyen seguro de viaje?')
        self.stdout.write('  Inquiries fixed')

        self.stdout.write(self.style.SUCCESS('All done!'))
