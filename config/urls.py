from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Personalizar Admin
admin.site.site_header = "Agencia de Turismo - Admin"
admin.site.site_title = "Admin Agencia"
admin.site.index_title = "Panel de Administración"

urlpatterns = [
    # Django Admin (solo para administradores)
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/auth/', include('applications.authentication.urls')),
    path('api/v1/destinations/', include('applications.destinations.urls')),
    path('api/v1/packages/', include('applications.packages.urls')),
    path('api/v1/hotels/', include('applications.hotels.urls')),
    path('api/v1/flights/', include('applications.flights.urls')),
    path('api/v1/activities/', include('applications.activities.urls')),
    path('api/v1/bookings/', include('applications.bookings.urls')),
    path('api/v1/reviews/', include('applications.reviews.urls')),
    path('api/v1/promotions/', include('applications.promotions.urls')),
    path('api/v1/inquiries/', include('applications.inquiries.urls')),
]

# Media files en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
