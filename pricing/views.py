from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PricingRule, Price, SpecialPrice
from .serializers import PricingRuleSerializer, PriceSerializer, SpecialPriceSerializer


class PricingRuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Pricing Rules API
    
    Endpoints:
    - GET /api/pricing-rules/ - List all pricing rules
    - POST /api/pricing-rules/ - Create a pricing rule
    - GET /api/pricing-rules/{id}/ - Get pricing rule details
    - PUT /api/pricing-rules/{id}/ - Update pricing rule
    - DELETE /api/pricing-rules/{id}/ - Delete pricing rule
    - POST /api/pricing-rules/{id}/activate/ - Activate rule
    - POST /api/pricing-rules/{id}/deactivate/ - Deactivate rule
    """
    queryset = PricingRule.objects.all()
    serializer_class = PricingRuleSerializer
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a pricing rule"""
        rule = self.get_object()
        rule.is_active = True
        rule.save()
        return Response({'message': f'Pricing rule {rule.rule_name} activated'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a pricing rule"""
        rule = self.get_object()
        rule.is_active = False
        rule.save()
        return Response({'message': f'Pricing rule {rule.rule_name} deactivated'})


class PriceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Prices API
    
    Endpoints:
    - GET /api/prices/ - List all prices
    - POST /api/prices/ - Create a price
    - GET /api/prices/{id}/ - Get price details
    - PUT /api/prices/{id}/ - Update price
    - DELETE /api/prices/{id}/ - Delete price
    - POST /api/prices/{id}/update-selling-price/ - Update selling price
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    
    @action(detail=True, methods=['post'])
    def update_selling_price(self, request, pk=None):
        """Update selling price"""
        price = self.get_object()
        new_price = request.data.get('selling_price')
        
        if new_price:
            price.selling_price = new_price
            # Recalculate discount percentage
            if price.listing_price > 0:
                price.discount_percentage = ((price.listing_price - float(new_price)) / price.listing_price) * 100
            price.save()
            
            serializer = self.get_serializer(price)
            return Response(serializer.data)
        
        return Response({'error': 'selling_price is required'}, status=status.HTTP_400_BAD_REQUEST)


class SpecialPriceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Special Prices API
    
    Endpoints:
    - GET /api/special-prices/ - List all special prices
    - POST /api/special-prices/ - Create a special price
    - GET /api/special-prices/{id}/ - Get special price details
    - PUT /api/special-prices/{id}/ - Update special price
    - DELETE /api/special-prices/{id}/ - Delete special price
    - POST /api/special-prices/{id}/activate/ - Activate special price
    - POST /api/special-prices/{id}/deactivate/ - Deactivate special price
    """
    queryset = SpecialPrice.objects.all()
    serializer_class = SpecialPriceSerializer
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a special price"""
        special_price = self.get_object()
        special_price.is_active = True
        special_price.save()
        return Response({'message': f'Special price {special_price.promotion_name} activated'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a special price"""
        special_price = self.get_object()
        special_price.is_active = False
        special_price.save()
        return Response({'message': f'Special price {special_price.promotion_name} deactivated'})
