from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from .models import Return, Replacement, RefundTransaction
from django.utils import timezone


class ReturnsService(ServiceBase):
    """SOAP Service for Returns API"""
    
    @rpc(Unicode, _returns=Unicode)
    def get_return(ctx, return_id):
        """Get return details by return ID"""
        try:
            return_request = Return.objects.get(return_id=return_id)
            return f"Return ID: {return_request.return_id}, Status: {return_request.status}, Refund Amount: {return_request.refund_amount}"
        except Return.DoesNotExist:
            return f"Return {return_id} not found"
    
    @rpc(_returns=Unicode)
    def list_returns(ctx):
        """List all returns"""
        returns = Return.objects.all()[:10]
        result = []
        for ret in returns:
            result.append(f"{ret.return_id}: {ret.status}")
        return ", ".join(result) if result else "No returns found"
    
    @rpc(Unicode, _returns=Unicode)
    def approve_return(ctx, return_id):
        """Approve a return request"""
        try:
            return_request = Return.objects.get(return_id=return_id)
            return_request.status = 'APPROVED'
            return_request.save()
            return f"Return {return_id} approved successfully"
        except Return.DoesNotExist:
            return f"Return {return_id} not found"
    
    @rpc(Unicode, _returns=Unicode)
    def reject_return(ctx, return_id):
        """Reject a return request"""
        try:
            return_request = Return.objects.get(return_id=return_id)
            return_request.status = 'REJECTED'
            return_request.save()
            return f"Return {return_id} rejected"
        except Return.DoesNotExist:
            return f"Return {return_id} not found"
    
    @rpc(Unicode, _returns=Unicode)
    def get_replacement(ctx, replacement_id):
        """Get replacement details"""
        try:
            replacement = Replacement.objects.get(replacement_id=replacement_id)
            return f"Replacement ID: {replacement.replacement_id}, Status: {replacement.status}, Tracking: {replacement.tracking_id}"
        except Replacement.DoesNotExist:
            return f"Replacement {replacement_id} not found"
    
    @rpc(Unicode, Unicode, _returns=Unicode)
    def dispatch_replacement(ctx, replacement_id, tracking_id):
        """Dispatch a replacement"""
        try:
            replacement = Replacement.objects.get(replacement_id=replacement_id)
            replacement.status = 'DISPATCHED'
            replacement.tracking_id = tracking_id
            replacement.save()
            return f"Replacement {replacement_id} dispatched with tracking ID: {tracking_id}"
        except Replacement.DoesNotExist:
            return f"Replacement {replacement_id} not found"
    
    @rpc(Unicode, _returns=Unicode)
    def get_refund_status(ctx, transaction_id):
        """Get refund transaction status"""
        try:
            refund = RefundTransaction.objects.get(transaction_id=transaction_id)
            return f"Transaction ID: {transaction_id}, Amount: {refund.refund_amount}, Status: {refund.refund_status}"
        except RefundTransaction.DoesNotExist:
            return f"Refund transaction {transaction_id} not found"
    
    @rpc(Unicode, _returns=Unicode)
    def complete_refund(ctx, transaction_id):
        """Complete a refund transaction"""
        try:
            refund = RefundTransaction.objects.get(transaction_id=transaction_id)
            refund.refund_status = 'COMPLETED'
            refund.completed_date = timezone.now()
            refund.save()
            return f"Refund {transaction_id} completed successfully"
        except RefundTransaction.DoesNotExist:
            return f"Refund transaction {transaction_id} not found"


# Create SOAP application
returns_soap_app = Application(
    [ReturnsService],
    tns='flipkart.seller.returns',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

returns_soap_application = DjangoApplication(returns_soap_app)
