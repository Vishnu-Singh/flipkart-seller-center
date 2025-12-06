from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Return, Replacement, RefundTransaction
from .serializers import ReturnSerializer, ReplacementSerializer, RefundTransactionSerializer


class ReturnViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Returns API
    
    Endpoints:
    - GET /api/returns/ - List all returns
    - POST /api/returns/ - Create a return request
    - GET /api/returns/{return_id}/ - Get return details
    - PUT /api/returns/{return_id}/ - Update return
    - DELETE /api/returns/{return_id}/ - Delete return
    - POST /api/returns/{return_id}/approve/ - Approve a return
    - POST /api/returns/{return_id}/reject/ - Reject a return
    - POST /api/returns/{return_id}/complete/ - Complete a return
    """
    queryset = Return.objects.all()
    serializer_class = ReturnSerializer
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a return request"""
        return_request = self.get_object()
        return_request.status = 'APPROVED'
        return_request.save()
        return Response({
            'message': f'Return {return_request.return_id} approved',
            'status': return_request.status
        })
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a return request"""
        return_request = self.get_object()
        return_request.status = 'REJECTED'
        return_request.save()
        return Response({
            'message': f'Return {return_request.return_id} rejected',
            'status': return_request.status
        })
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete a return"""
        return_request = self.get_object()
        return_request.status = 'COMPLETED'
        return_request.save()
        return Response({
            'message': f'Return {return_request.return_id} completed',
            'status': return_request.status
        })


class ReplacementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Replacements API
    
    Endpoints:
    - GET /api/replacements/ - List all replacements
    - POST /api/replacements/ - Create a replacement
    - GET /api/replacements/{replacement_id}/ - Get replacement details
    - PUT /api/replacements/{replacement_id}/ - Update replacement
    - DELETE /api/replacements/{replacement_id}/ - Delete replacement
    - POST /api/replacements/{replacement_id}/dispatch/ - Dispatch replacement
    - POST /api/replacements/{replacement_id}/complete/ - Complete replacement
    """
    queryset = Replacement.objects.all()
    serializer_class = ReplacementSerializer
    
    @action(detail=True, methods=['post'])
    def dispatch(self, request, pk=None):
        """Dispatch a replacement"""
        replacement = self.get_object()
        replacement.status = 'DISPATCHED'
        replacement.tracking_id = request.data.get('tracking_id', '')
        replacement.save()
        return Response({
            'message': f'Replacement {replacement.replacement_id} dispatched',
            'tracking_id': replacement.tracking_id
        })
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete a replacement"""
        replacement = self.get_object()
        replacement.status = 'COMPLETED'
        replacement.save()
        return Response({
            'message': f'Replacement {replacement.replacement_id} completed',
            'status': replacement.status
        })


class RefundTransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Refund Transactions API
    
    Endpoints:
    - GET /api/refund-transactions/ - List all refund transactions
    - POST /api/refund-transactions/ - Create a refund transaction
    - GET /api/refund-transactions/{transaction_id}/ - Get refund transaction details
    - PUT /api/refund-transactions/{transaction_id}/ - Update refund transaction
    - POST /api/refund-transactions/{transaction_id}/process/ - Process refund
    - POST /api/refund-transactions/{transaction_id}/complete/ - Complete refund
    """
    queryset = RefundTransaction.objects.all()
    serializer_class = RefundTransactionSerializer
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Process a refund"""
        refund = self.get_object()
        refund.refund_status = 'PROCESSED'
        refund.save()
        return Response({
            'message': f'Refund {refund.transaction_id} processed',
            'status': refund.refund_status
        })
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete a refund"""
        refund = self.get_object()
        refund.refund_status = 'COMPLETED'
        refund.completed_date = timezone.now()
        refund.save()
        return Response({
            'message': f'Refund {refund.transaction_id} completed',
            'status': refund.refund_status
        })
