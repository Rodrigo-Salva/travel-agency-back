from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Personalizar Admin
admin.site.site_header = "Agencia de Turismo - Admin"
admin.site.site_title = "Admin Agencia"
admin.site.index_title = "Panel de Administración"

urlpatterns = [
    path('api/v1/auth/', include('applications.authentication.urls')),
    #path('api/v1/destinations/', include('apps.destinations.urls')),
    #path('api/v1/packages/', include('apps.packages.urls')),
    path('api/v1/hotels/', include('applications.hotels.urls')),
    path('api/v1/flights/', include('applications.flights.urls')),
    #path('api/v1/activities/', include('apps.activities.urls')),
    #path('api/v1/bookings/', include('apps.bookings.urls')),
    #path('api/v1/reviews/', include('apps.reviews.urls')),
    #path('api/v1/promotions/', include('apps.promotions.urls')),
    #path('api/v1/inquiries/', include('apps.inquiries.urls')),
    path('api/v1/bookings/', include('applications.bookings.urls')),
]

# Media files en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
