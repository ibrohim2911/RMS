import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F
from order.models import Order

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Processes pending inventory deductions for paid orders'

    def handle(self, *args, **options):
        self.stdout.write("Checking for orders pending inventory deduction...")
        
        # Get all orders that are paid/closed and haven't had inventory deducted
        orders = Order.objects.filter(status__in=['paid', 'closed'], inventory_deducted=False)
        count = orders.count()
        if count == 0:
            self.stdout.write("No pending orders to process.")
            return

        self.stdout.write(f"Found {count} orders to process.")

        for order in orders:
            try:
                with transaction.atomic():
                    # Process each item in the order
                    for item in order.items.filter(is_deleted=False):
                        # Find the BOM for the menu item
                        bom_items = item.menu_item.resources.all()
                        for bom in bom_items:
                            # Calculate total raw resource to deduct
                            total_qty_to_deduct = bom.quantity * item.quantity
                            
                            # Deduct from the Resource
                            resource = bom.resource
                            resource.quantity = F('quantity') - total_qty_to_deduct
                            resource.save()
                    
                    # Mark order as deducted
                    order.inventory_deducted = True
                    order.save()
                    self.stdout.write(self.style.SUCCESS(f"Successfully deducted inventory for Order {order.id}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to process inventory for Order {order.id}: {e}"))
