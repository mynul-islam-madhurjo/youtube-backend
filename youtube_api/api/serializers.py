from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.conf import settings
import os
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

class VideoUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for video upload with file validation
    Handles both video file and thumbnail upload
    """
    video_file = serializers.FileField(required=True)
    thumbnail_file = serializers.ImageField(required=False)
    
    class Meta:
        model = Video
        fields = [
            'title', 'description', 'video_file', 'thumbnail_file',
            'category', 'channel', 'status', 'is_shorts'
        ]
    
    def validate_video_file(self, value):
        """
        Validate video file size and format
        
        Args:
            value: Uploaded video file
            
        Returns:
            File object if valid
            
        Raises:
            ValidationError: If file is invalid
        """
        # Check file size
        if hasattr(settings, 'MAX_VIDEO_SIZE'):
            if value.size > settings.MAX_VIDEO_SIZE:
                size_mb = settings.MAX_VIDEO_SIZE / (1024 * 1024)
                raise serializers.ValidationError(
                    f"Video file too large. Maximum size is {size_mb}MB."
                )
        
        # Check file extension
        ext = os.path.splitext(value.name)[1].lower()
        if hasattr(settings, 'ALLOWED_VIDEO_EXTENSIONS'):
            if ext not in settings.ALLOWED_VIDEO_EXTENSIONS:
                raise serializers.ValidationError(
                    f"Unsupported video format. Allowed formats: {', '.join(settings.ALLOWED_VIDEO_EXTENSIONS)}"
                )
        
        return value
    
    def validate_thumbnail_file(self, value):
        """
        Validate thumbnail file if provided
        
        Args:
            value: Uploaded thumbnail file
            
        Returns:
            File object if valid
            
        Raises:
            ValidationError: If file is invalid
        """
        if value:
            # Check file size (max 10MB for thumbnails)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError(
                    "Thumbnail file too large. Maximum size is 10MB."
                )
            
            # Check file extension
            ext = os.path.splitext(value.name)[1].lower()
            if hasattr(settings, 'ALLOWED_IMAGE_EXTENSIONS'):
                if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
                    raise serializers.ValidationError(
                        f"Unsupported image format. Allowed formats: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}"
                    )
        
        return value
    
    def create(self, validated_data):
        """
        Create new video with uploaded files
        
        Args:
            validated_data: Validated form data
            
        Returns:
            Video: Created video instance
        """
        # Set initial status to processing
        validated_data['status'] = 'processing'
        
        video = Video.objects.create(**validated_data)
        
        # Here you could add background processing logic
        # For now, we'll just mark it as published
        video.status = 'published'
        video.save()
        
        return video

class VideoSerializer(serializers.ModelSerializer):
    """Serializer for Video model (list view)"""
    channel = ChannelSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    views_display = serializers.ReadOnlyField()
    uploaded_display = serializers.ReadOnlyField()
    video_url = serializers.ReadOnlyField()
    thumbnail_url = serializers.ReadOnlyField()
    file_size_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'thumbnail', 'thumbnail_url', 'video_url', 
            'duration', 'views', 'views_display', 'uploaded_display', 
            'channel', 'category', 'file_size_display', 'status'
        ]

class VideoDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed Video model (single video view)"""
    channel = ChannelSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    views_display = serializers.ReadOnlyField()
    uploaded_display = serializers.ReadOnlyField()
    video_url = serializers.ReadOnlyField()
    thumbnail_url = serializers.ReadOnlyField()
    file_size_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description', 'thumbnail', 'thumbnail_url', 
            'video_url', 'duration', 'views', 'views_display', 'likes', 
            'dislikes', 'uploaded_display', 'channel', 'category', 
            'is_live', 'is_shorts', 'file_size_display', 'status'
        ]