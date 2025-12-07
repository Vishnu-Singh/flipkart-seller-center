from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, OrderItem, OrderCancellation
from .serializers import OrderSerializer, OrderItemSerializer, OrderCancellationSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Orders API
    
    Endpoints:
    - GET /api/orders/ - List all orders
    - POST /api/orders/ - Create a new order
    - GET /api/orders/{order_id}/ - Get order details
    - PUT /api/orders/{order_id}/ - Update order
    - DELETE /api/orders/{order_id}/ - Delete order
    - POST /api/orders/{order_id}/cancel/ - Cancel an order
    - POST /api/orders/{order_id}/dispatch/ - Mark order as dispatched
    - GET /api/orders/{order_id}/track/ - Track order
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        reason = request.data.get('reason', '')
        cancelled_by = request.data.get('cancelled_by', 'SELLER')
        refund_amount = request.data.get('refund_amount', order.total_amount)
        
        cancellation = OrderCancellation.objects.create(
            order=order,
            cancellation_id=f"CANC-{order.order_id}",
            reason=reason,
            cancelled_by=cancelled_by,
            refund_amount=refund_amount
        )
        
        order.status = 'CANCELLED'
        order.save()
        
        return Response({
            'message': 'Order cancelled successfully',
            'cancellation_id': cancellation.cancellation_id
        })
    
    @action(detail=True, methods=['post'])
    def dispatch(self, request, pk=None):
        """Mark order as dispatched"""
        order = self.get_object()
        order.status = 'READY_TO_DISPATCH'
        order.save()
        
        return Response({
            'message': 'Order marked for dispatch',
            'order_id': order.order_id,
            'status': order.status
        })
    
    @action(detail=True, methods=['get'])
    def track(self, request, pk=None):
        """Track order status"""
        order = self.get_object()
        return Response({
            'order_id': order.order_id,
            'status': order.status,
            'order_date': order.order_date,
            'last_updated': order.updated_at
        })


class OrderItemViewSet(viewsets.ModelViewSet):
    """ViewSet for Order Items"""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderCancellationViewSet(viewsets.ModelViewSet):
    """ViewSet for Order Cancellations"""
    queryset = OrderCancellation.objects.all()
    serializer_class = OrderCancellationSerializer
