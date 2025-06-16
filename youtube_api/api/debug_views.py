"""
Debug views for troubleshooting upload issues
"""
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Video
import logging
import os

logger = logging.getLogger(__name__)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def debug_upload(request):
    """
    Debug endpoint to see what data is being received
    """
    try:
        logger.info("=== DEBUG UPLOAD REQUEST ===")
        logger.info(f"Request method: {request.method}")
        logger.info(f"Content type: {request.content_type}")
        logger.info(f"Request data keys: {list(request.data.keys())}")
        logger.info(f"Request files keys: {list(request.FILES.keys())}")
        
        # Log all form data
        for key, value in request.data.items():
            logger.info(f"Data[{key}]: {value} (type: {type(value)})")
        
        # Log all files
        for key, file in request.FILES.items():
            logger.info(f"File[{key}]: {file.name} - Size: {file.size} bytes - Type: {file.content_type}")
        
        return Response({
            'status': 'debug_success',
            'received_data': dict(request.data),
            'received_files': {k: {
                'name': v.name,
                'size': v.size,
                'content_type': v.content_type
            } for k, v in request.FILES.items()},
            'message': 'Debug data logged successfully'
        })
        
    except Exception as e:
        logger.error(f"Debug upload error: {str(e)}")
        return Response({
            'status': 'debug_error',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def debug_video_file(request, video_id):
    """
    Debug endpoint to check video file status
    """
    try:
        video = Video.objects.get(id=video_id)
        
        file_info = {
            'video_id': video.id,
            'title': video.title,
            'video_file': str(video.video_file) if video.video_file else None,
            'video_file_name': video.video_file.name if video.video_file else None,
            'video_url': video.video_url,
            'file_size': video.file_size,
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