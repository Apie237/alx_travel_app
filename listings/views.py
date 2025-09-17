from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Listing, Review, Booking
from .serializers import ListingSerializer, ReviewSerializer, BookingSerializer

class ListingListCreateView(generics.ListCreateAPIView):
    """
    List all listings or create a new listing.
    """
    queryset = Listing.objects.filter(is_available=True)
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property_type', 'location', 'max_guests']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price_per_night', 'created_at']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a listing instance.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

class ReviewListCreateView(generics.ListCreateAPIView):
    """
    List all reviews for a listing or create a new review.
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        listing_id = self.kwargs['listing_id']
        return Review.objects.filter(listing_id=listing_id)
    
    def perform_create(self, serializer):
        listing_id = self.kwargs['listing_id']
        serializer.save(reviewer=self.request.user, listing_id=listing_id)

class BookingListCreateView(generics.ListCreateAPIView):
    """
    List all bookings or create a new booking.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a booking instance.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_overview(self, request):
    """
    API Overview - List all available endpoints
    """
    api_urls = {
        'List/Create Listings': '/api/listings/',
        'Listing Detail': '/api/listings/<int:pk>/',
        'List/Create Reviews': '/api/listings/<int:listing_id>/reviews/',
        'List/Create Bookings': '/api/bookings/',
        'Booking Detail': '/api/bookings/<int:pk>/',
        'API Documentation': '/swagger/',
        'ReDoc Documentation': '/redoc/',
    }
    return Response(api_urls)