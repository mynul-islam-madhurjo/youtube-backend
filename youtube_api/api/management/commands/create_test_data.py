"""
Management command to create test data for development
Creates basic channels and categories needed for video uploads
"""
from django.core.management.base import BaseCommand
from api.models import Channel, Category


class Command(BaseCommand):
    help = 'Creates test data for development'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...')
        
        # Create test categories
        categories = [
            {'name': 'Music', 'slug': 'music'},
            {'name': 'Gaming', 'slug': 'gaming'},
            {'name': 'Education', 'slug': 'education'},
            {'name': 'Entertainment', 'slug': 'entertainment'},
            {'name': 'Technology', 'slug': 'technology'},
            {'name': 'Sports', 'slug': 'sports'},
        ]
        
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')
        
        # Create test channels
        channels = [
            {
                'name': 'Default Channel',
                'handle': '@defaultchannel',
                'subscribers': 1000,
                'verified': False,
                'description': 'Default channel for testing'
            },
            {
                'name': 'Tech Channel',
                'handle': '@techchannel',
                'subscribers': 50000,
                'verified': True,
                'description': 'Technology and programming content'
            },
            {
                'name': 'Music Channel',
                'handle': '@musicchannel',
                'subscribers': 25000,
                'verified': False,
                'description': 'Music and entertainment content'
            }
        ]
        
        for chan_data in channels:
            channel, created = Channel.objects.get_or_create(
                handle=chan_data['handle'],
                defaults=chan_data
            )
            if created:
                self.stdout.write(f'Created channel: {channel.name} (ID: {channel.id})')
            else:
                self.stdout.write(f'Channel already exists: {channel.name} (ID: {channel.id})')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created test data!')
        )
        
        # Show available channels
        self.stdout.write('\nAvailable channels:')
        for channel in Channel.objects.all():
            self.stdout.write(f'  ID: {channel.id}, Name: {channel.name}, Handle: {channel.handle}') 