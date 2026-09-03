import json
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from users.models import User
from order.models import Order, OrderItem
from inventory.models import MenuItem

logger = logging.getLogger(__name__)

class OrderConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.restaurant_id = None
        self.group_name = None
        await self.accept()
        logger.info("WebSocket connection accepted.")

    async def disconnect(self, close_code):
        if self.group_name:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            logger.info(f"Disconnected from group {self.group_name}")

    async def receive_json(self, content, **kwargs):
        pin = content.get('pin')
        action = content.get('action')

        if not pin or not action:
            await self.send_json({"status": "error", "message": "Missing pin or action"})
            return

        user = await self.get_user_by_pin(pin)
        if not user:
            await self.send_json({"status": "error", "message": "Invalid PIN"})
            return

        # Ensure we are in the restaurant group
        if not self.group_name and user.restaurant_id:
            self.restaurant_id = str(user.restaurant_id)
            self.group_name = f"restaurant_{self.restaurant_id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            logger.info(f"Joined group {self.group_name}")

        if action == 'ping':
            await self.send_json({
                "status": "success",
                "message": "pong",
                "user": user.name,
                "restaurant_id": self.restaurant_id
            })
        elif action == 'add_item':
            order_id = content.get('order_id')
            menu_item_id = content.get('menu_item_id')
            quantity = content.get('quantity', 1)
            
            if not order_id or not menu_item_id:
                await self.send_json({"status": "error", "message": "Missing order_id or menu_item_id"})
                return
                
            try:
                order_item_id = await self.add_item_to_order(order_id, menu_item_id, quantity, user)
                
                # Broadcast update
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "order_updated",
                        "order_id": order_id,
                        "action": "item_added",
                        "item_id": str(order_item_id)
                    }
                )
            except Exception as e:
                logger.error(f"Error adding item: {e}")
                await self.send_json({"status": "error", "message": str(e)})
        else:
            await self.send_json({"status": "error", "message": "Unknown action"})

    async def order_updated(self, event):
        # Send event down to the client
        await self.send_json(event)

    @database_sync_to_async
    def get_user_by_pin(self, pin):
        try:
            # We filter by pin, and since pin is unique it should return exactly one user
            return User.objects.select_related('restaurant').get(pin=pin)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def add_item_to_order(self, order_id, menu_item_id, quantity, user):
        order = Order.objects.get(id=order_id, restaurant=user.restaurant)
        menu_item = MenuItem.objects.get(id=menu_item_id, restaurant=user.restaurant)
        
        # Create order item
        item = OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=quantity,
            price=menu_item.price * quantity,
            orderer=user,
            restaurant=user.restaurant
        )
        return item.id
