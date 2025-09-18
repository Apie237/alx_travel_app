from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Listing, Review, Booking, ListingImage

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'full_name']
        read_only_fields = ['id']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

class ListingImageSerializer(serializers.ModelSerializer):
    """Serializer for Listing Images"""
    
    class Meta:
        model = ListingImage
        fields = ['id', 'image', 'caption', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Reviews"""
    reviewer = UserSerializer(read_only=True)
    reviewer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = [
            'id', 'reviewer', 'reviewer_name', 'rating', 'title', 
            'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_reviewer_name(self, obj):
        return obj.reviewer.get_full_name() or obj.reviewer.username

class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listings"""
    host = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)
    amenities_list = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'property_type', 'location', 
            'address', 'latitude', 'longitude', 'price_per_night', 
            'max_guests', 'bedrooms', 'bathrooms', 'amenities', 
            'amenities_list', 'host', 'is_available', 'created_at', 
            'updated_at', 'reviews', 'images', 'average_rating', 'total_reviews'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'host']
    
    def validate_price_per_night(self, value):
        """Validate price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price per night must be greater than 0.")
        return value
    
    def validate_max_guests(self, value):
        """Validate max guests is reasonable"""
        if value < 1:
            raise serializers.ValidationError("Maximum guests must be at least 1.")
        if value > 50:
            raise serializers.ValidationError("Maximum guests cannot exceed 50.")
        return value

class ListingCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating listings (simplified)"""
    
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'property_type', 'location', 
            'address', 'latitude', 'longitude', 'price_per_night', 
            'max_guests', 'bedrooms', 'bathrooms', 'amenities', 'is_available'
        ]

class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Bookings"""
    guest = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.IntegerField(write_only=True)
    nights_count = serializers.ReadOnlyField(source='total_nights')
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_id', 'guest', 'check_in_date', 
            'check_out_date', 'num_guests', 'guest_name', 'guest_email', 
            'guest_phone', 'price_per_night', 'total_nights', 'nights_count',
            'subtotal', 'tax_amount', 'total_price', 'status', 
            'special_requests', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'guest', 'price_per_night',
            'total_nights', 'subtotal', 'tax_amount', 'total_price'
        ]
    
    def validate(self, data):
        """Validate booking data"""
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        
        if check_in and check_out:
            if check_in >= check_out:
                raise serializers.ValidationError({
                    'check_out_date': "Check-out date must be after check-in date."
                })
            
            if check_in < timezone.now().date():
                raise serializers.ValidationError({
                    'check_in_date': "Check-in date cannot be in the past."
                })
        
        # Validate listing exists and is available
        listing_id = data.get('listing_id')
        if listing_id:
            try:
                listing = Listing.objects.get(id=listing_id)
                if not listing.is_available:
                    raise serializers.ValidationError({
                        'listing_id': "This property is not available for booking."
                    })
                
                num_guests = data.get('num_guests', 1)
                if num_guests > listing.max_guests:
                    raise serializers.Validation