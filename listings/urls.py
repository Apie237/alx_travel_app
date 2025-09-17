from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.api_overview, name='api-overview'),
    path('listings/', views.ListingListCreateView.as_view(), name='listing-list-create'),
    path('listings/<int:pk>/', views.ListingDetailView.as_view(), name='listing-detail'),
    path('listings/<int:listing_id>/reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('bookings/', views.BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
]
```

### listings/admin.py
```python
from django.contrib import admin
from .models import Listing, Review, Booking

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'location', 'price_per_night', 'host', 'is_available', 'created_at']
    list_filter = ['property_type', 'is_available', 'created_at']
    search_fields = ['title', 'location', 'host__username']
    list_editable = ['is_available']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'property_type', 'location')
        }),
        ('Property Details', {
            'fields': ('price_per_night', 'max_guests', 'bedrooms', 'bathrooms', 'amenities')
        }),
        ('Management', {
            'fields': ('host', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['listing', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['listing__title', 'reviewer__username']
    readonly_fields = ['created_at']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['listing', 'guest', 'check_in_date', 'check_out_date', 'status', 'total_price']
    list_filter = ['status', 'check_in_date', 'created_at']
    search_fields = ['listing__title', 'guest__username']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']