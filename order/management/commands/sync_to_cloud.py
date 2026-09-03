import os
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from order.models import Order
from order.serializers import OrderSerializer

class Command(BaseCommand):
    help = 'Syncs offline POS data to the Cloud VPS'

    def handle(self, *args, **options):
        if settings.SERVER_ROLE != 'LOCAL':
            self.stdout.write(self.style.WARNING("Server role is not LOCAL. Aborting sync."))
            return
            
        if not settings.BRANCH_API_KEY:
            self.stdout.write(self.style.ERROR("BRANCH_API_KEY not set!"))
            return

        unsynced_orders = Order.objects.filter(is_synced=False)
        if not unsynced_orders.exists():
            self.stdout.write(self.style.SUCCESS("No unsynced orders found."))
            return

        # Use the serializer to recursively convert the order, items, and payments to dicts
        serializer = OrderSerializer(unsynced_orders, many=True)
        payload = serializer.data
        
        headers = {
            'Authorization': f'Bearer {settings.BRANCH_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        try:
            self.stdout.write(f"Syncing {len(payload)} orders to {settings.CLOUD_SYNC_URL}...")
            response = requests.post(settings.CLOUD_SYNC_URL, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                synced_count = response.json().get('synced_count', 0)
                unsynced_orders.update(is_synced=True)
                self.stdout.write(self.style.SUCCESS(f"Successfully synced {synced_count} orders to the cloud!"))
            else:
                self.stdout.write(self.style.ERROR(f"Sync failed: HTTP {response.status_code} - {response.text}"))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Connection error: {e}"))
