from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Video, Channel, Category
from .serializers import VideoSerializer, VideoDetailSerializer, ChannelSerializer, CategorySerializer

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
        
        # Base queryset
        videos = Video.objects.select_related('channel', 'category').all()
        
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
        return Response({
            'status': 'error',
            'message': str(e)
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
            video = Video.objects.select_related('channel', 'category').get(id=video_id)
        else:
            # Get featured/random video for homepage
            video = Video.objects.select_related('channel', 'category').first()
        
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
    Returns recommended videos for the sidebar
    """
    try:
        # Get current video to base recommendations on
        current_video = Video.objects.get(id=video_id)
        
        # Get recommended videos (same category, different videos)
        recommended = Video.objects.select_related('channel', 'category').filter(
            category=current_video.category
        ).exclude(id=video_id)[:10]
        
        # If not enough from same category, add popular videos
        if recommended.count() < 10:
            additional = Video.objects.select_related('channel', 'category').exclude(
                id__in=[v.id for v in recommended]
            ).exclude(id=current_video.id).order_by('-views')[:10-recommended.count()]
            
            recommended = list(recommended) + list(additional)
        
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