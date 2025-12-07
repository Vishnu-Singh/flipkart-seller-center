from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.views.decorators.csrf import csrf_exempt
from .models import Shipment, ShipmentTracking, CourierPartner
from django.utils import timezone


class ShipmentsService(ServiceBase):
    """SOAP Service for Shipments API"""
    
    @rpc(Unicode, _returns=Unicode)
    def get_shipment(ctx, shipment_id):
        """Get shipment details by shipment ID"""
        try:
            shipment = Shipment.objects.get(shipment_id=shipment_id)
            return f"Shipment ID: {shipment.shipment_id}, Tracking: {shipment.tracking_number}, Status: {shipment.status}, Courier: {shipment.courier_partner}"
        except Shipment.DoesNotExist:
            return f"Shipment {shipment_id} not found"
    
    @rpc(Unicode, _returns=Unicode)
    def track_shipment(ctx, tracking_number):
        """Track shipment by tracking number"""
        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number)
            events = shipment.tracking_events.all()[:5]
            
            result = [f"Shipment ID: {shipment.shipment_id}, Status: {shipment.status}"]
            for event in events:
                result.append(f"{event.event_date.strftime('%Y-%m-%d %H:%M')} - {event.location}: {event.event_description}")
            
            return " | ".join(result)
        except Shipment.DoesNotExist:
            return f"Shipment with tracking number {tracking_number} not found"
    
    @rpc(Unicode, _returns=Unicode)
    def dispatch_shipment(ctx, shipment_id):
        """Dispatch a shipment"""
        try:
            shipment = Shipment.objects.get(shipment_id=shipment_id)
            shipment.status = 'SHIPPED'
            shipment.save()
            
            ShipmentTracking.objects.create(
                shipment=shipment,
                event_date=timezone.now(),
                location='Seller Location',
                event_description='Shipment dispatched',
                status_code='DISPATCHED'
            )
            
            return f"Shipment {shipment_id} dispatched successfully"
        except Shipment.DoesNotExist:
            return f"Shipment {shipment_id} not found"
    
    @rpc(Unicode, _returns=Unicode)
    def deliver_shipment(ctx, shipment_id):
        """Mark shipment as delivered"""
        try:
            shipment = Shipment.objects.get(shipment_id=shipment_id)
            shipment.status = 'DELIVERED'
            shipment.actual_delivery_date = timezone.now()
            shipment.save()
            
            ShipmentTracking.objects.create(
                shipment=shipment,
                event_date=timezone.now(),
                location='Delivery Location',
                event_description='Shipment delivered',
                status_code='DELIVERED'
            )
            
            return f"Shipment {shipment_id} marked as delivered"
        except Shipment.DoesNotExist:
            return f"Shipment {shipment_id} not found"
    
    @rpc(_returns=Unicode)
    def list_courier_partners(ctx):
        """List all active courier partners"""
        partners = CourierPartner.objects.filter(is_active=True)
        result = []
        for partner in partners:
            result.append(f"{partner.partner_name} ({partner.partner_code})")
        return ", ".join(result) if result else "No active courier partners found"
    
    @rpc(Unicode, _returns=Unicode)
    def get_courier_partner(ctx, partner_code):
        """Get courier partner details"""
        try:
            partner = CourierPartner.objects.get(partner_code=partner_code)
            return f"Partner: {partner.partner_name}, Code: {partner.partner_code}, Service: {partner.service_type}, Contact: {partner.contact_number}"
        except CourierPartner.DoesNotExist:
            return f"Courier partner {partner_code} not found"


# Create SOAP application
shipments_soap_app = Application(
    [ShipmentsService],
    tns='flipkart.seller.shipments',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

shipments_soap_application = csrf_exempt(DjangoApplication(shipments_soap_app))
