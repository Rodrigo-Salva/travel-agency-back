from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, timedelta

from applications.destinations.models import Destination
from .models import Wishlist, Package, Category

User = get_user_model()


def make_destination():
    return Destination.objects.create(
        name='Lima',
        country='Perú',
        continent='América del Sur',
        description='Capital del Perú',
        short_description='Lima, Perú',
        latitude=-12.046374,
        longitude=-77.042793,
        best_season='Todo el año',
    )


def make_package(destination=None):
    if destination is None:
        destination = make_destination()
    category = Category.objects.create(name='Aventura')
    return Package.objects.create(
        name='Paquete Test',
        description='Descripción de prueba',
        short_description='Desc corta',
        category=category,
        destination=destination,
        duration_days=5,
        duration_nights=4,
        price_adult=1000,
        price_child=700,
        max_people=20,
        available_from=date.today(),
        available_until=date.today() + timedelta(days=60),
    )


class WishlistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.package = make_package()

    def test_wishlist_creation(self):
        wishlist = Wishlist.objects.create(user=self.user, package=self.package)
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
        self.package = make_package()

    def test_list_wishlist_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/promotions/wishlists/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_wishlist_unauthenticated(self):
        response = self.client.get('/api/promotions/wishlists/')
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )

    def test_add_to_wishlist(self):
        self.client.force_authenticate(user=self.user)
        data = {'package': self.package.id}
        response = self.client.post('/api/promotions/wishlists/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_toggle_wishlist(self):
        self.client.force_authenticate(user=self.user)
        data = {'package': self.package.id}
        response = self.client.post('/api/promotions/wishlists/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        wishlist_id = response.data['favorito']['id']
        response = self.client.delete(f'/api/promotions/wishlists/{wishlist_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
