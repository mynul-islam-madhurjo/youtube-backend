from rest_framework import serializers
from .models import Video, Channel, Category

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ChannelSerializer(serializers.ModelSerializer):
    """Serializer for Channel model"""
    subscribers_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Channel
        fields = [
            'id', 'name', 'handle', 'subscribers', 
            'subscribers_display', 'verified', 'avatar', 'description'
        ]

class VideoSerializer(serializers.ModelSerializer):
    """Serializer for Video model (list view)"""
    channel = ChannelSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    views_display = serializers.ReadOnlyField()
    uploaded_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'thumbnail', 'duration', 'views', 
            'views_display', 'uploaded_display', 'channel', 'category'
        ]

class VideoDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed Video model (single video view)"""
    channel = ChannelSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    views_display = serializers.ReadOnlyField()
    uploaded_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description', 'thumbnail', 'duration', 
            'views', 'views_display', 'likes', 'dislikes', 
            'uploaded_display', 'channel', 'category', 'is_live', 'is_shorts'
        ]