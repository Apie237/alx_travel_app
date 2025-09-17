from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Review, Booking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

class ListingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'property_type', 'location',
            'price_per_night', 'max_guests', 'bedrooms', 'bathrooms',
            'amenities', 'host', 'is_available', 'created_at', 'updated_at',
            'reviews', 'average_rating', 'total_reviews'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    def get_total_reviews(self, obj):
        return obj.reviews.count()

class BookingSerializer(serializers.ModelSerializer):
    guest = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_id', 'guest', 'check_in_date',
            'check_out_date', 'num_guests', 'total_price', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_price']
    
    def validate(self, data):
        if data['check_in_date'] >= data['check_out_date']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        return data