from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Shipment, ShipmentTracking, ShippingLabel, CourierPartner
from .serializers import (
    ShipmentSerializer, ShipmentTrackingSerializer,
    ShippingLabelSerializer, CourierPartnerSerializer
)


class ShipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Shipments API
    
    Endpoints:
    - GET /api/shipments/ - List all shipments
    - POST /api/shipments/ - Create a shipment
    - GET /api/shipments/{shipment_id}/ - Get shipment details
    - PUT /api/shipments/{shipment_id}/ - Update shipment
    - DELETE /api/shipments/{shipment_id}/ - Delete shipment
    - GET /api/shipments/{shipment_id}/track/ - Track shipment
    - POST /api/shipments/{shipment_id}/dispatch/ - Dispatch shipment
    - POST /api/shipments/{shipment_id}/deliver/ - Mark as delivered
    """
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    
    @action(detail=True, methods=['get'])
    def track(self, request, pk=None):
        """Track shipment"""
        shipment = self.get_object()
        tracking_events = shipment.tracking_events.all()
        serializer = ShipmentTrackingSerializer(tracking_events, many=True)
        
        return Response({
            'shipment_id': shipment.shipment_id,
            'tracking_number': shipment.tracking_number,
            'status': shipment.status,
            'courier_partner': shipment.courier_partner,
            'tracking_events': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def dispatch(self, request, pk=None):
        """Dispatch a shipment"""
        shipment = self.get_object()
        shipment.status = 'SHIPPED'
        shipment.save()
        
        # Create tracking event
        ShipmentTracking.objects.create(
            shipment=shipment,
            event_date=timezone.now(),
            location=request.data.get('location', 'Seller Location'),
            event_description='Shipment dispatched',
            status_code='DISPATCHED'
        )
        
        return Response({
            'message': f'Shipment {shipment.shipment_id} dispatched',
            'status': shipment.status
        })
    
    @action(detail=True, methods=['post'])
    def deliver(self, request, pk=None):
        """Mark shipment as delivered"""
        shipment = self.get_object()
        shipment.status = 'DELIVERED'
        shipment.actual_delivery_date = timezone.now()
        shipment.save()
        
        # Create tracking event
        ShipmentTracking.objects.create(
            shipment=shipment,
            event_date=timezone.now(),
            location=request.data.get('location', 'Delivery Location'),
            event_description='Shipment delivered',
            status_code='DELIVERED'
        )
        
        return Response({
            'message': f'Shipment {shipment.shipment_id} delivered',
            'delivery_date': shipment.actual_delivery_date
        })


class ShipmentTrackingViewSet(viewsets.ModelViewSet):
    """ViewSet for Shipment Tracking Events"""
    queryset = ShipmentTracking.objects.all()
    serializer_class = ShipmentTrackingSerializer


class ShippingLabelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Shipping Labels API
    
    Endpoints:
    - GET /api/shipping-labels/ - List all shipping labels
    - POST /api/shipping-labels/ - Create a shipping label
    - GET /api/shipping-labels/{id}/ - Get shipping label details
    - PUT /api/shipping-labels/{id}/ - Update shipping label
    """
    queryset = ShippingLabel.objects.all()
    serializer_class = ShippingLabelSerializer


class CourierPartnerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Courier Partners API
    
    Endpoints:
    - GET /api/courier-partners/ - List all courier partners
    - POST /api/courier-partners/ - Create a courier partner
    - GET /api/courier-partners/{id}/ - Get courier partner details
    - PUT /api/courier-partners/{id}/ - Update courier partner
    - POST /api/courier-partners/{id}/activate/ - Activate courier partner
    - POST /api/courier-partners/{id}/deactivate/ - Deactivate courier partner
    """
    queryset = CourierPartner.objects.all()
    serializer_class = CourierPartnerSerializer
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a courier partner"""
        partner = self.get_object()
        partner.is_active = True
        partner.save()
        return Response({'message': f'Courier partner {partner.partner_name} activated'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a courier partner"""
        partner = self.get_object()
        partner.is_active = False
        partner.save()
        return Response({'message': f'Courier partner {partner.partner_name} deactivated'})
