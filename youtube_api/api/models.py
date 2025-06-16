from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.conf import settings
import os
import uuid

class Category(models.Model):
    """
    Category model for video filtering (All, Music, Gaming, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Channel(models.Model):
    """
    Channel model representing YouTube channels/creators
    """
    name = models.CharField(max_length=100, unique=True)
    handle = models.CharField(max_length=100, unique=True, default='@channel')
    description = models.TextField(blank=True)
    avatar = models.CharField(max_length=500, blank=True)
    subscribers = models.PositiveIntegerField(default=0)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    @property
    def subscribers_display(self):
        """Format subscriber count for display"""
        if self.subscribers >= 1000000:
            return f"{self.subscribers / 1000000:.1f}M subscribers"
        elif self.subscribers >= 1000:
            return f"{self.subscribers / 1000:.1f}K subscribers"
        return f"{self.subscribers} subscribers"

def video_upload_path(instance, filename):
    """
    Generate upload path for video files
    Returns: videos/{channel_id}/{uuid}_{filename}
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}_{filename}"
    return os.path.join('videos', str(instance.channel.id), filename)

def thumbnail_upload_path(instance, filename):
    """
    Generate upload path for thumbnail files
    Returns: thumbnails/{channel_id}/{uuid}_{filename}
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}_{filename}"
    return os.path.join('thumbnails', str(instance.channel.id), filename)

class Video(models.Model):
    """
    Video model representing individual videos
    """
    # Basic info
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    
    # File fields - Actual file storage
    video_file = models.FileField(
        upload_to=video_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'])],
        help_text="Upload video file (max 500MB)"
    )
    thumbnail_file = models.ImageField(
        upload_to=thumbnail_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])],
        help_text="Upload thumbnail image"
    )
    
    # Legacy fields for backward compatibility
    thumbnail = models.CharField(max_length=500, blank=True)
    
    # Video metadata
    duration = models.CharField(max_length=10, blank=True)
    file_size = models.PositiveBigIntegerField(default=0, help_text="File size in bytes")
    video_quality = models.CharField(max_length=10, default="1080p")
    
    # Stats
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    
    # Timestamps
    upload_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(null=True, blank=True)
    
    # Relationships
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Status and type
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('processing', 'Processing'),
        ('published', 'Published'),
        ('private', 'Private'),
        ('unlisted', 'Unlisted'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_live = models.BooleanField(default=False)
    is_shorts = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return self.title
    
    @property
    def video_url(self):
        """Return the video file URL"""
        if self.video_file:
            # For uploaded files, use the MEDIA_URL
            return f"/media/{self.video_file.name}"
        # Fallback to static files for legacy/mock data
        return '/static/videos/file_example_MP4_1280_10MG.mp4'
    
    @property
    def thumbnail_url(self):
        """Return the thumbnail file URL"""
        if self.thumbnail_file:
            # For uploaded thumbnails, use the MEDIA_URL
            return f"/media/{self.thumbnail_file.name}"
        elif self.thumbnail:  # Fallback to legacy field
            return self.thumbnail
        return "/static/thumbnails/default.jpg"
    
    @property
    def file_size_display(self):
        """Format file size for display"""
        if self.file_size >= 1024 * 1024 * 1024:  # GB
            return f"{self.file_size / (1024 * 1024 * 1024):.1f} GB"
        elif self.file_size >= 1024 * 1024:  # MB
            return f"{self.file_size / (1024 * 1024):.1f} MB"
        elif self.file_size >= 1024:  # KB
            return f"{self.file_size / 1024:.1f} KB"
        return f"{self.file_size} bytes"
    
    @property
    def views_display(self):
        """Format view count for display (e.g., 1.2M views, 850K views)"""
        if self.views >= 1000000:
            return f"{self.views / 1000000:.1f}M views"
        elif self.views >= 1000:
            return f"{self.views / 1000:.1f}K views"
        return f"{self.views} views"
    
    @property
    def uploaded_display(self):
        """Format upload time for display (e.g., 2 days ago, 1 week ago)"""
        now = timezone.now()
        diff = now - self.upload_date
        
        if diff.days == 0:
            hours = diff.seconds // 3600
            if hours == 0:
                minutes = diff.seconds // 60
                return f"{minutes} minutes ago" if minutes > 1 else "1 minute ago"
            return f"{hours} hours ago" if hours > 1 else "1 hour ago"
        elif diff.days < 7:
            return f"{diff.days} days ago" if diff.days > 1 else "1 day ago"
        elif diff.days < 30:
            weeks = diff.days // 7
            return f"{weeks} weeks ago" if weeks > 1 else "1 week ago"
        elif diff.days < 365:
            months = diff.days // 30
            return f"{months} months ago" if months > 1 else "1 month ago"
        else:
            years = diff.days // 365
            return f"{years} years ago" if years > 1 else "1 year ago"

    def save(self, *args, **kwargs):
        """Override save to handle file processing"""
        if self.video_file and not self.file_size:
            self.file_size = self.video_file.size
        
        # Auto-publish if not specified
        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()
            
        super().save(*args, **kwargs)
