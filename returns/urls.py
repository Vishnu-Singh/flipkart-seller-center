from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReturnViewSet, ReplacementViewSet, RefundTransactionViewSet
from .soap_views import returns_soap_application

# REST API Router
router = DefaultRouter()
router.register(r'returns', ReturnViewSet, basename='return')
router.register(r'replacements', ReplacementViewSet, basename='replacement')
router.register(r'refund-transactions', RefundTransactionViewSet, basename='refundtransaction')

urlpatterns = [
    # REST API endpoints
    path('api/', include(router.urls)),
    
    # SOAP API endpoint
    path('soap/', returns_soap_application),
]
