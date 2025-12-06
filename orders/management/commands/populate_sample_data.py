"""
Management command to populate the database with sample data for testing.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from orders.models import Order, OrderItem, OrderCancellation
from inventory.models import Product, Inventory, Listing
from pricing.models import Price, PricingRule, SpecialPrice
from returns.models import Return, Replacement, RefundTransaction
from shipments.models import Shipment, ShipmentTracking, ShippingLabel, CourierPartner
from reports.models import Report, ScheduledReport, ReportMetrics


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data population...')
        
        # Clear existing data (optional)
        self.stdout.write('Creating sample data...')
        
        # Create Products
        products = []
        for i in range(1, 6):
            product, created = Product.objects.get_or_create(
                sku=f'SKU-{1000+i}',
                defaults={
                    'fsn': f'FSN-{2000+i}',
                    'product_name': f'Product {i}',
                    'description': f'Description for product {i}',
                    'brand': f'Brand {(i % 3) + 1}',
                    'category': 'Electronics' if i <= 3 else 'Fashion',
                    'subcategory': 'Mobile' if i <= 2 else 'Laptop',
                    'mrp': Decimal(str(1000 * i)),
                    'hsn_code': f'HSN{1000+i}',
                    'tax_percentage': Decimal('18.00'),
                    'is_active': True
                }
            )
            products.append(product)
            if created:
                self.stdout.write(f'  Created product: {product.sku}')
        
        # Create Inventory
        for product in products:
            inventory, created = Inventory.objects.get_or_create(
                product=product,
                defaults={
                    'available_quantity': 100,
                    'reserved_quantity': 10,
                    'damaged_quantity': 5,
                    'warehouse_location': 'WH-001',
                    'procurement_sla': 7
                }
            )
            if created:
                self.stdout.write(f'  Created inventory for: {product.sku}')
        
        # Create Listings
        for product in products:
            listing, created = Listing.objects.get_or_create(
                product=product,
                listing_id=f'LIST-{product.sku}',
                defaults={
                    'marketplace': 'Flipkart',
                    'listing_status': 'ACTIVE',
                    'fulfillment_type': 'FBF',
                    'shipping_charges': Decimal('50.00'),
                    'is_cod_available': True
                }
            )
            if created:
                self.stdout.write(f'  Created listing: {listing.listing_id}')
        
        # Create Prices
        for product in products:
            price, created = Price.objects.get_or_create(
                product=product,
                defaults={
                    'listing_price': product.mrp,
                    'selling_price': product.mrp * Decimal('0.9'),
                    'discount_percentage': Decimal('10.00'),
                    'cost_price': product.mrp * Decimal('0.6'),
                    'commission_percentage': Decimal('15.00'),
                    'shipping_fee': Decimal('50.00')
                }
            )
            if created:
                self.stdout.write(f'  Created price for: {product.sku}')
        
        # Create Courier Partners
        courier_partners = []
        for i, name in enumerate(['BlueDart', 'DTDC', 'FedEx'], 1):
            partner, created = CourierPartner.objects.get_or_create(
                partner_code=f'CP-{i}',
                defaults={
                    'partner_name': name,
                    'contact_number': f'1800-{1000+i}',
                    'email': f'{name.lower()}@example.com',
                    'service_type': 'Express',
                    'is_active': True
                }
            )
            courier_partners.append(partner)
            if created:
                self.stdout.write(f'  Created courier partner: {name}')
        
        # Create Orders
        for i in range(1, 4):
            order, created = Order.objects.get_or_create(
                order_id=f'ORD-{10000+i}',
                defaults={
                    'order_date': timezone.now() - timedelta(days=i),
                    'status': 'APPROVED',
                    'customer_name': f'Customer {i}',
                    'customer_email': f'customer{i}@example.com',
                    'customer_phone': f'98765432{i}0',
                    'shipping_address': f'{i} Main Street, City, State',
                    'billing_address': f'{i} Main Street, City, State',
                    'total_amount': Decimal(str(5000 * i)),
                    'payment_method': 'UPI' if i % 2 == 0 else 'COD'
                }
            )
            if created:
                self.stdout.write(f'  Created order: {order.order_id}')
                
                # Create Order Items
                for j, product in enumerate(products[:2], 1):
                    OrderItem.objects.create(
                        order=order,
                        sku=product.sku,
                        product_name=product.product_name,
                        quantity=j,
                        unit_price=product.mrp,
                        total_price=product.mrp * j,
                        hsn_code=product.hsn_code
                    )
        
        # Create Shipments
        orders = Order.objects.all()[:2]
        for i, order in enumerate(orders, 1):
            shipment, created = Shipment.objects.get_or_create(
                shipment_id=f'SHIP-{20000+i}',
                defaults={
                    'order': order,
                    'tracking_number': f'TRK-{30000+i}',
                    'courier_partner': courier_partners[i % len(courier_partners)].partner_name,
                    'shipment_date': timezone.now() - timedelta(days=i-1),
                    'expected_delivery_date': timezone.now() + timedelta(days=3),
                    'status': 'SHIPPED',
                    'pickup_address': 'Seller Address',
                    'delivery_address': order.shipping_address,
                    'weight': Decimal('1.5'),
                    'dimensions': '10x10x10',
                    'shipping_charges': Decimal('50.00')
                }
            )
            if created:
                self.stdout.write(f'  Created shipment: {shipment.shipment_id}')
                
                # Create Tracking Event
                ShipmentTracking.objects.create(
                    shipment=shipment,
                    event_date=timezone.now(),
                    location='Mumbai Hub',
                    event_description='Shipment dispatched from seller',
                    status_code='DISPATCHED'
                )
        
        # Create Reports
        for i, report_type in enumerate(['SALES', 'ORDERS', 'INVENTORY'], 1):
            report, created = Report.objects.get_or_create(
                report_id=f'RPT-{40000+i}',
                defaults={
                    'report_type': report_type,
                    'report_name': f'{report_type} Report {i}',
                    'report_format': 'CSV' if i % 2 == 0 else 'XLSX',
                    'status': 'COMPLETED',
                    'start_date': (timezone.now() - timedelta(days=30)).date(),
                    'end_date': timezone.now().date(),
                    'file_url': f'https://example.com/reports/{report_type.lower()}_report.csv',
                    'file_size': 1024 * 100 * i,
                    'completed_at': timezone.now(),
                    'requested_by': 'Admin'
                }
            )
            if created:
                self.stdout.write(f'  Created report: {report.report_id}')
        
        # Create Scheduled Reports
        for i, frequency in enumerate(['DAILY', 'WEEKLY', 'MONTHLY'], 1):
            scheduled, created = ScheduledReport.objects.get_or_create(
                schedule_id=f'SCH-{50000+i}',
                defaults={
                    'report_type': 'SALES',
                    'report_name': f'{frequency} Sales Report',
                    'report_format': 'XLSX',
                    'frequency': frequency,
                    'next_run_date': timezone.now() + timedelta(days=i),
                    'is_active': True,
                    'email_recipients': 'admin@example.com, seller@example.com'
                }
            )
            if created:
                self.stdout.write(f'  Created scheduled report: {scheduled.schedule_id}')
        
        self.stdout.write(self.style.SUCCESS('✓ Sample data populated successfully!'))
        self.stdout.write(self.style.SUCCESS('✓ You can now test the API endpoints.'))
