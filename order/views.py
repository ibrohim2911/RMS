from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem, OrderPayment
from .serializers import OrderSerializer, OrderItemSerializer, OrderPaymentSerializer
from log.models import Log
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_orders'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_orders'
        return super().get_permissions()
    @action(detail=True, methods=['post'])
    def add_item(self,request, pk=None):
        order = self.get_object()
        menu_item_id = request.data.get('menu_item_id')
        quantity = request.data.get('quantity')
        if not menu_item_id:
            return Response({'error': 'menu_item_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not quantity:
            return Response({'error': 'quantity is required'}, status=status.HTTP_400_BAD_REQUEST)

        if order.status in ['paid', 'closed']:
            return Response({'error': 'Cannot add items to a paid or closed order'}, status=status.HTTP_400_BAD_REQUEST)
        if order.status == 'pre-closed':
            order.status = 'open'
            order.save()
        order_item = OrderItem.objects.create(order=order, menu_item_id=menu_item_id, quantity=quantity, orderer=request.user)
        serializer = OrderItemSerializer(order_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @action(detail=True, methods=['post'])
    def add_payment(self,request, pk=None):
        order = self.get_object()
        amount = request.data.get('amount')
        method = request.data.get('method')
        if not amount:
            return Response({'error': 'amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not method:
            return Response({'error': 'method is required'}, status=status.HTTP_400_BAD_REQUEST)
        order_payment = OrderPayment.objects.create(order=order, amount=amount, method=method)
        if order_payment.amount >= order.total_amount:
            order.status = 'paid'
            order.save()
        else:
            order.status = 'closed'
            order.save()
        serializer = OrderPaymentSerializer(order_payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @action(detail=True, methods=['post'])
    def full_payment(self, request, pk=None):
        order = self.get_object()
        total_amount = order.total_amount
        method = request.data.get('method')
        if total_amount <= 0:
            return Response({'error': 'Order is already fully paid'}, status=status.HTTP_400_BAD_REQUEST)
        if not method:
            return Response({'error': 'method is required'}, status=status.HTTP_400_BAD_REQUEST)
        order_payment = OrderPayment.objects.create(order=order, amount=total_amount, method=method)
        serializer = OrderPaymentSerializer(order_payment)
        order.status = 'paid'
        order.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_order_items'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_order_items'
        return super().get_permissions()
    @action(detail=True, methods=['post'])
    def cut_item(self, request, pk=None):
        order_item = self.get_object()
        cut  = request.data.get('cut')
        if cut is None:
            return Response({'error': 'cut is required'}, status=status.HTTP_400_BAD_REQUEST)
        if cut <= 0 or cut >= order_item.quantity:
            return Response({'error': 'cut must be greater than 0 and less than the current quantity'}, status=status.HTTP_400_BAD_REQUEST)
        new_order_item = OrderItem.objects.create(
            order=order_item.order,
            menu_item=order_item.menu_item,
            quantity= cut,)
        order_item.quantity -= cut
        order_item.save()
        serializer = OrderItemSerializer(new_order_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
class OrderPaymentViewSet(viewsets.ModelViewSet):
    queryset = OrderPayment.objects.all()
    serializer_class = OrderPaymentSerializer
    def get_permissions(self):
        # Set required_permission based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_permission = 'manage_order_payments'
        elif self.action in ['list', 'retrieve']:
            self.required_permission = 'view_order_payments'
        return super().get_permissions()
    