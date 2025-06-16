from django.urls import path
from . import views
from . import debug_views

urlpatterns = [
    path('getvideos/', views.get_videos, name='get_videos'),
    path('getvideodata/', views.get_video_data, name='get_video_data_featured'),
    path('getvideodata/<int:video_id>/', views.get_video_data, name='get_video_data'),
    path('categories/', views.get_categories, name='get_categories'),
    path('channels/', views.get_channels, name='get_channels'),
    path('recommended/<int:video_id>/', views.get_recommended_videos, name='get_recommended_videos'),
    path('search/', views.search_videos, name='search_videos'),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('my_videos/', views.get_my_videos, name='get_my_videos'),
    path('video/<int:video_id>/', views.delete_video, name='delete_video'),
    
    # Debug endpoints
    path('debug_upload/', debug_views.debug_upload, name='debug_upload'),
    path('debug/video/<int:video_id>/', views.debug_video_file, name='debug_video_file'),
]
