from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.utils import timezone
import logging
from .models import Video, Channel, Category
from .serializers import (
    VideoSerializer, VideoDetailSerializer, VideoUploadSerializer,
    ChannelSerializer, CategorySerializer
)
import os
from django.conf import settings

# Configure logging
logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_videos(request):
    """
    GET /api/getvideos
    Returns a list of videos for the home page grid
    Supports filtering by category and search
    """
    try:
        # Get query parameters
        category = request.GET.get('category', None)
        search = request.GET.get('search', None)
        limit = request.GET.get('limit', 20)
        
        # Base queryset - only show published videos
        videos = Video.objects.select_related('channel', 'category').filter(
            status='published'
        )
        
        # Filter by category if provided
        if category and category.lower() != 'all':
            videos = videos.filter(category__slug=category)
        
        # Search functionality
        if search:
            videos = videos.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(channel__name__icontains=search)
            )
        
        # Limit results
        videos = videos[:int(limit)]
        
        # Serialize data
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        
        return Response({
            'status': 'success',
            'count': len(serializer.data),
            'data': serializer.data
        })
        
    except Exception as e:
        logger.error(f"Error fetching videos: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_video(request):
    """
    POST /api/upload_video
    Upload a new video with metadata
    
    Expected form data:
    - video_file: Video file (required)
    - thumbnail_file: Thumbnail image (optional)
    - title: Video title (required)
    - description: Video description (optional)
    - category: Category ID (optional)
    - channel: Channel ID (required)
    - is_shorts: Boolean for shorts videos
    """
    try:
        logger.info(f"Video upload request received from user")
        
        # Log received data for debugging
        logger.debug(f"Files: {request.FILES}")
        logger.debug(f"Data: {request.data}")
        
        serializer = VideoUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the video
            video = serializer.save()
            
            logger.info(f"Video uploaded successfully: {video.id} - {video.title}")
            
            # Return the created video data
            response_serializer = VideoDetailSerializer(video, context={'request': request})
            
            return Response({
                'status': 'success',
                'message': 'Video uploaded successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        else:
            logger.warning(f"Video upload validation failed: {serializer.errors}")
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Error uploading video: {str(e)}")
        return Response({
            'status': 'error',
            'message': 'Failed to upload video',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_video_data(request, video_id=None):
    """
    GET /api/getvideodata/{id}
    Returns detailed video metadata for a specific video
    """
    try:
        if video_id:
            # Get specific video
            video = Video.objects.select_related('channel', 'category').get(
                id=video_id, status='published'
            )
            
            # Increment view count
            video.views += 1
            video.save(update_fields=['views'])
            
        else:
            # Get featured/random video for homepage
            video = Video.objects.select_related('channel', 'category').filter(
                status='published'
            ).first()
        
        if not video:
            return Response({
                'status': 'error',
                'message': 'Video not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize detailed video data
        serializer = VideoDetailSerializer(video, context={'request': request})
        
        return Response({
            'status': 'success',
            'data': serializer.data
        })
        
    except Video.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Video not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error fetching video data: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_my_videos(request):
    """
    GET /api/my_videos?channel={channel_id}
    Get videos uploaded by a specific channel
    """
    try:
        channel_id = request.GET.get('channel')
        if not channel_id:
            return Response({
                'status': 'error',
                'message': 'Channel ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        videos = Video.objects.select_related('channel', 'category').filter(
            channel_id=channel_id
        ).order_by('-upload_date')
        
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        
        return Response({
            'status': 'success',
            'count': len(serializer.data),
            'data': serializer.data
        })
        
    except Exception as e:
        logger.error(f"Error fetching channel videos: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_video(request, video_id):
    """
    DELETE /api/video/{id}
    Delete a video (only by the owner)
    """
    try:
        video = Video.objects.get(id=video_id)
        
        # Here you would add authentication/authorization checks
        # For now, we'll allow anyone to delete
        
        # Delete associated files
        if video.video_file:
            video.video_file.delete(save=False)
        if video.thumbnail_file:
            video.thumbnail_file.delete(save=False)
        
        video.delete()
        
        logger.info(f"Video deleted: {video_id}")
        
        return Response({
            'status': 'success',
            'message': 'Video deleted successfully'
        })
        
    except Video.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Video not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error deleting video: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_categories(request):
    """
    GET /api/categories
    Returns list of categories for filter chips
    """
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        
        return Response({
            'status': 'success',
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_recommended_videos(request, video_id):
    """
    GET /api/recommended/{video_id}
    Returns recommended videos for the sidebar based on similar tags/category
    """
    try:
        # Get current video to base recommendations on
        current_video = Video.objects.get(id=video_id, status='published')
        
        # Start with videos from the same category
        recommended = Video.objects.select_related('channel', 'category').filter(
            category=current_video.category,
            status='published'
        ).exclude(id=video_id).order_by('-views')[:5]
        
        # If not enough from same category, add popular videos from other categories
        if recommended.count() < 10:
            additional = Video.objects.select_related('channel', 'category').filter(
                status='published'
            ).exclude(
                id__in=[v.id for v in recommended]
            ).exclude(id=current_video.id).order_by('-views')[:10-recommended.count()]
            
            recommended = list(recommended) + list(additional)
        
        # If still not enough, add more recent videos
        if len(recommended) < 10:
            recent = Video.objects.select_related('channel', 'category').filter(
                status='published'
            ).exclude(
                id__in=[v.id for v in recommended]
            ).exclude(id=current_video.id).order_by('-upload_date')[:10-len(recommended)]
            
            recommended = recommended + list(recent)
        
        serializer = VideoSerializer(recommended, many=True, context={'request': request})
        
        return Response({
            'status': 'success',
            'data': serializer.data
        })
        
    except Video.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Video not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error fetching recommended videos: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def search_videos(request):
    """
    GET /api/search?q={query}
    Search videos by title, description, or channel name
    """
    try:
        query = request.GET.get('q', '')
        if not query:
            return Response({
                'status': 'error',
                'message': 'Search query is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Search videos
        videos = Video.objects.select_related('channel', 'category').filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(channel__name__icontains=query)
        )[:20]
        
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        
        return Response({
            'status': 'success',
            'query': query,
            'count': len(serializer.data),
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_channels(request):
    """
    GET /api/channels
    Returns list of channels for upload form
    """
    try:
        channels = Channel.objects.all().order_by('name')
        serializer = ChannelSerializer(channels, many=True)
        
        return Response({
            'status': 'success',
            'data': serializer.data
        })
        
    except Exception as e:
        logger.error(f"Error fetching channels: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def debug_video_file(request, video_id):
    """
    Debug endpoint to check video file status and create missing directories
    """
    try:
        video = Video.objects.get(id=video_id)
        
        # Ensure media directories exist
        video_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
        os.makedirs(video_dir, exist_ok=True)
        
        file_info = {
            'video_id': video.id,
            'title': video.title,
            'video_file': str(video.video_file) if video.video_file else None,
            'video_file_name': video.video_file.name if video.video_file else None,
            'video_url': video.video_url,
            'file_size': video.file_size,
            'file_size_display': video.file_size_display,
            'media_root': settings.MEDIA_ROOT,
            'media_url': settings.MEDIA_URL,
        }
        
        # Check if file exists on filesystem
        if video.video_file:
            file_path = video.video_file.path
            file_info['file_path'] = file_path
            file_info['file_exists'] = os.path.exists(file_path)
            if os.path.exists(file_path):
                file_info['actual_file_size'] = os.path.getsize(file_path)
            else:
                file_info['error'] = 'File not found on disk'
        else:
            file_info['error'] = 'No video file associated with this video'
        
        return Response({
            'status': 'success',
            'data': file_info
        })
        
    except Video.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Video not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Debug video file error: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)