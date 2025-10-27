from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, timedelta

from applications.packages.models import Wishlist, Package, Category
from applications.destinations.models import Destination

User = get_user_model()


class WishlistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(name='Test Category')
        self.destination = Destination.objects.create(
            name='Test Destination',
            country='Test Country',
            description='Test Description',
            short_description='Short description',
            latitude=0.0,
            longitude=0.0
        )
        
        self.package = Package.objects.create(
            name='Paquete Test',
            description='Descripción de prueba',
            short_description='Descripción corta',
            category=self.category,
            destination=self.destination,
            duration_days=5,
            duration_nights=4,
            price_adult=1000.00,
            price_child=500.00,
            max_people=10,
            min_people=2,
            available_from=date.today(),
            available_until=date.today() + timedelta(days=365)
        )
    
    def test_wishlist_creation(self):
        wishlist = Wishlist.objects.create(
            user=self.user,
            package=self.package
        )
        self.assertEqual(wishlist.user, self.user)
        self.assertEqual(wishlist.package, self.package)
    
    def test_wishlist_unique_constraint(self):
        Wishlist.objects.create(user=self.user, package=self.package)
        with self.assertRaises(Exception):
            Wishlist.objects.create(user=self.user, package=self.package)


class WishlistAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(name='Test Category')
        self.destination = Destination.objects.create(
            name='Test Destination',
            country='Test Country',
            description='Test Description',
            short_description='Short description',
            latitude=0.0,
            longitude=0.0
        )
        
        self.package = Package.objects.create(
            name='Paquete Test',
            description='Descripción de prueba',
            short_description='Descripción corta',
            category=self.category,
            destination=self.destination,
            duration_days=5,
            duration_nights=4,
            price_adult=1000.00,
            price_child=500.00,
            max_people=10,
            min_people=2,
            available_from=date.today(),
            available_until=date.today() + timedelta(days=365)
        )
    
    def test_list_wishlist_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/packages/wishlist/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_wishlist_unauthenticated(self):
        response = self.client.get('/api/packages/wishlist/')
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )
    
    def test_add_to_wishlist(self):
        self.client.force_authenticate(user=self.user)
        data = {'package_id': self.package.id}
        response = self.client.post('/api/packages/wishlist/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_wishlist_count(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/packages/wishlist/count/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
    
    def test_toggle_wishlist(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/packages/wishlist/toggle/{self.package.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['in_wishlist'])
        
        response = self.client.post(f'/api/packages/wishlist/toggle/{self.package.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['in_wishlist'])