"""
Management command to seed the database with sample YouTube data
Usage: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from api.models import Category, Channel, Video
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Seed the database with sample YouTube data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed database...'))
        
        # Create Categories
        categories_data = [
            {'name': 'All', 'slug': 'all'},
            {'name': 'Music', 'slug': 'music'},
            {'name': 'Gaming', 'slug': 'gaming'},
            {'name': 'Sports', 'slug': 'sports'},
            {'name': 'News', 'slug': 'news'},
            {'name': 'Movies', 'slug': 'movies'},
            {'name': 'Live', 'slug': 'live'},
            {'name': 'Education', 'slug': 'education'},
            {'name': 'Technology', 'slug': 'technology'},
            {'name': 'Comedy', 'slug': 'comedy'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create Channels
        channels_data = [
            {
                'name': 'TechVision',
                'handle': '@techvision',
                'subscribers': 620000,
                'verified': True,
                'avatar': '/avatars/figma.png',  
                'description': 'Latest technology trends and reviews'
            },
            {
                'name': 'CodeWithMe',
                'handle': '@codewithme',
                'subscribers': 450000,
                'verified': True,
                'avatar': '/avatars/timgabe.jpg', 
                'description': 'Programming tutorials and coding tips'
            },
            {
                'name': 'GameMaster',
                'handle': '@gamemaster',
                'subscribers': 1200000,
                'verified': True,
                'avatar': '/avatars/kole.jpg',  
                'description': 'Gaming content and reviews'
            },
            {
                'name': 'MusicVibes',
                'handle': '@musicvibes',
                'subscribers': 890000,
                'verified': True,
                'avatar': '/avatars/freecodecamp.jpg',  
                'description': 'Latest music and artist interviews'
            },
            {
                'name': 'SportsCenter',
                'handle': '@sportscenter',
                'subscribers': 2100000,
                'verified': True,
                'avatar': '/avatars/uxpeak.jpg',  
                'description': 'Sports highlights and analysis'
            },
        ]
        
        for channel_data in channels_data:
            channel, created = Channel.objects.get_or_create(
                handle=channel_data['handle'],
                defaults=channel_data
            )
            if created:
                self.stdout.write(f'Created channel: {channel.name}')

        # Create Videos
        videos_data = [
            {
                'title': 'Top 10 AI Tools You Should Know',
                'description': 'Discover the most powerful AI tools that can boost your productivity...',
                'thumbnail': '/thumbnails/video1.jpg',
                'duration': '12:34',
                'views': 3250000,
                'likes': 94000,
                'channel_handle': '@techvision',
                'category_slug': 'technology'
            },
            {
                'title': 'How to Learn Python Fast',
                'description': 'Complete Python tutorial for beginners. Learn Python programming...',
                'thumbnail': '/thumbnails/video2.png',
                'duration': '15:42',
                'views': 120000,
                'likes': 5600,
                'channel_handle': '@codewithme',
                'category_slug': 'education'
            },
            {
                'title': 'Best Games of 2024',
                'description': 'Top 10 games you must play this year. From indie gems to AAA titles...',
                'thumbnail': '/thumbnails/video3.jpg',
                'duration': '18:25',
                'views': 850000,
                'likes': 42000,
                'channel_handle': '@gamemaster',
                'category_slug': 'gaming'
            },
            {
                'title': 'Latest Music Hits 2024',
                'description': 'The hottest tracks of 2024. New releases and trending songs...',
                'thumbnail': '/thumbnails/video4.jpg',
                'duration': '45:12',
                'views': 2100000,
                'likes': 78000,
                'channel_handle': '@musicvibes',
                'category_slug': 'music'
            },
            {
                'title': 'Championship Highlights',
                'description': 'Best moments from the championship game. Incredible plays...',
                'thumbnail': '/thumbnails/video5.jpg',
                'duration': '8:33',
                'views': 1800000,
                'likes': 65000,
                'channel_handle': '@sportscenter',
                'category_slug': 'sports'
            },
            {
                'title': 'React vs Vue in 2024',
                'description': 'Complete comparison of React and Vue.js frameworks...',
                'thumbnail': '/thumbnails/video6.jpg',
                'duration': '22:15',
                'views': 380000,
                'likes': 18000,
                'channel_handle': '@codewithme',
                'category_slug': 'technology'
            },
            {
                'title': 'Mobile Game Development Tips',
                'description': 'Essential tips for creating successful mobile games...',
                'thumbnail': '/thumbnails/video7.jpg',
                'duration': '16:48',
                'views': 420000,
                'likes': 22000,
                'channel_handle': '@gamemaster',
                'category_slug': 'gaming'
            },
            {
                'title': 'AI in Music Production',
                'description': 'How artificial intelligence is changing music creation...',
                'thumbnail': '/thumbnails/video8.jpg',
                'duration': '13:27',
                'views': 650000,
                'likes': 35000,
                'channel_handle': '@musicvibes',
                'category_slug': 'music'
            },
        ]
        
        for video_data in videos_data:
            try:
                channel = Channel.objects.get(handle=video_data['channel_handle'])
                category = Category.objects.get(slug=video_data['category_slug'])
                
                video, created = Video.objects.get_or_create(
                    title=video_data['title'],
                    defaults={
                        'description': video_data['description'],
                        'thumbnail': video_data['thumbnail'],
                        'duration': video_data['duration'],
                        'views': video_data['views'],
                        'likes': video_data['likes'],
                        'channel': channel,
                        'category': category,
                        'upload_date': timezone.now() - timezone.timedelta(days=random.randint(1, 30))
                    }
                )
                if created:
                    self.stdout.write(f'Created video: {video.title}')
            except (Channel.DoesNotExist, Category.DoesNotExist) as e:
                self.stdout.write(self.style.ERROR(f'Error creating video {video_data["title"]}: {e}'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!')) 