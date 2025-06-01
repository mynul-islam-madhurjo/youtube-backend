from django.urls import path
from . import views

urlpatterns = [
    path('getvideos/', views.get_videos, name='get_videos'),
    path('getvideodata/', views.get_video_data, name='get_video_data'),
    path('getvideodata/<int:video_id>/', views.get_video_data, name='get_video_data_by_id'),
    path('categories/', views.get_categories, name='get_categories'),
    path('recommended/<int:video_id>/', views.get_recommended_videos, name='get_recommended_videos'),
    path('search/', views.search_videos, name='search_videos'),
]
