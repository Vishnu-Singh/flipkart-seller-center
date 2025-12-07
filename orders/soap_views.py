from spyne import Application, rpc, ServiceBase, Unicode, Integer, Decimal, DateTime
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem, OrderCancellation
from django.utils import timezone


class OrderService(ServiceBase):
    """SOAP Service for Orders API"""
    
    @rpc(Unicode, _returns=Unicode)
    def get_order(ctx, order_id):
        """Get order details by order ID"""
        try:
            order = Order.objects.get(order_id=order_id)
            return f"Order ID: {order.order_id}, Status: {order.status}, Total: {order.total_amount}"
        except Order.DoesNotExist:
            return f"Order {order_id} not found"
    
    @rpc(_returns=Unicode)
    def list_orders(ctx):
        """List all orders"""
        orders = Order.objects.all()[:10]  # Limit to 10 for SOAP
        result = []
        for order in orders:
            result.append(f"{order.order_id}: {order.status}")
        return ", ".join(result) if result else "No orders found"
    
    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def cancel_order(ctx, order_id, reason, cancelled_by):
        """Cancel an order"""
        try:
            order = Order.objects.get(order_id=order_id)
            cancellation = OrderCancellation.objects.create(
                order=order,
                cancellation_id=f"CANC-{order_id}",
                reason=reason,
                cancelled_by=cancelled_by,
                refund_amount=order.total_amount
            )
            order.status = 'CANCELLED'
            order.save()
            return f"Order {order_id} cancelled successfully. Cancellation ID: {cancellation.cancellation_id}"
        except Order.DoesNotExist:
            return f"Order {order_id} not found"
    
    @rpc(Unicode, _returns=Unicode)
    def dispatch_order(ctx, order_id):
        """Mark order as ready to dispatch"""
        try:
            order = Order.objects.get(order_id=order_id)
            order.status = 'READY_TO_DISPATCH'
            order.save()
            return f"Order {order_id} marked for dispatch"
        except Order.DoesNotExist:
            return f"Order {order_id} not found"
    
    @rpc(Unicode, _returns=Unicode)
    def track_order(ctx, order_id):
        """Track order status"""
        try:
            order = Order.objects.get(order_id=order_id)
            return f"Order {order_id} - Status: {order.status}, Last Updated: {order.updated_at}"
        except Order.DoesNotExist:
            return f"Order {order_id} not found"


# Create SOAP application
orders_soap_app = Application(
    [OrderService],
    tns='flipkart.seller.orders',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

orders_soap_application = csrf_exempt(DjangoApplication(orders_soap_app))
