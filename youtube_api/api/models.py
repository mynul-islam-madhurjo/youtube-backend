from django.db import models
from django.utils import timezone
import os

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
    Channel model representing YouTube channels
    """
    name = models.CharField(max_length=200)
    handle = models.CharField(max_length=100, unique=True)  # @username
    subscribers = models.PositiveIntegerField(default=0)
    verified = models.BooleanField(default=False)
    avatar = models.CharField(max_length=500, blank=True)  # Path to avatar image
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def subscribers_display(self):
        """Format subscriber count for display (e.g., 1.2M, 850K)"""
        if self.subscribers >= 1000000:
            return f"{self.subscribers / 1000000:.1f}M"
        elif self.subscribers >= 1000:
            return f"{self.subscribers / 1000:.1f}K"
        return str(self.subscribers)

class Video(models.Model):
    """
    Video model representing individual videos
    """
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    thumbnail = models.CharField(max_length=500)  # Path to thumbnail image
    duration = models.CharField(max_length=10)  # Format: "12:34"
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    upload_date = models.DateTimeField(default=timezone.now)
    
    # Relationships
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Additional fields
    is_live = models.BooleanField(default=False)
    is_shorts = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return self.title
    
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
