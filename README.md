# Flipkart Seller Center API

A comprehensive Django-based application implementing Flipkart Seller Center APIs with both REST and SOAP endpoints.

## 📚 Documentation

**Complete interactive documentation is available at: `http://localhost:8000/docs/`**

The documentation app provides:
- Quick start guides
- Detailed setup instructions
- Complete API reference for all endpoints
- Code examples
- Troubleshooting guides
- Changelog

## Project Overview

This project provides a complete API suite for managing Flipkart seller operations, organized into six main API classifications:

1. **Orders API** - Manage orders, shipments, and cancellations
2. **Inventory API** - Manage products, inventory, and listings
3. **Pricing API** - Manage pricing, special prices, and pricing rules
4. **Returns API** - Handle returns, replacements, and refunds
5. **Shipments API** - Manage shipments, tracking, and courier partners
6. **Reports API** - Generate and download reports

## Features

- **Django Apps**: Each API classification is implemented as a separate Django app
- **REST API**: Full RESTful API with Django REST Framework
- **SOAP API**: SOAP endpoints using Spyne for legacy system integration
- **Comprehensive Models**: Well-structured database models for all entities
- **Viewsets**: Complete CRUD operations with custom actions
- **Interactive Documentation**: Web-based documentation with examples
- **API Documentation**: Browsable REST API and WSDL for SOAP

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Vishnu-Singh/flipkart-seller-center.git
cd flipkart-seller-center
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Access the application at `http://localhost:8000/`

## API Structure

### Orders API

**REST Endpoints:**
- `GET /orders/api/orders/` - List all orders
- `POST /orders/api/orders/` - Create a new order
- `GET /orders/api/orders/{order_id}/` - Get order details
- `PUT /orders/api/orders/{order_id}/` - Update order
- `POST /orders/api/orders/{order_id}/cancel/` - Cancel an order
- `POST /orders/api/orders/{order_id}/dispatch/` - Mark order as dispatched
- `GET /orders/api/orders/{order_id}/track/` - Track order

**SOAP Endpoint:**
- `POST /orders/soap/` - SOAP service endpoint
- WSDL: `/orders/soap/?wsdl`

### Inventory API

**REST Endpoints:**
- `GET /inventory/api/products/` - List all products
- `POST /inventory/api/products/` - Create a product
- `GET /inventory/api/products/{sku}/` - Get product details
- `POST /inventory/api/products/{sku}/activate/` - Activate product
- `GET /inventory/api/inventory/` - List inventory
- `POST /inventory/api/inventory/{id}/update-stock/` - Update stock
- `GET /inventory/api/listings/` - List all listings

**SOAP Endpoint:**
- `POST /inventory/soap/`
- WSDL: `/inventory/soap/?wsdl`

### Pricing API

**REST Endpoints:**
- `GET /pricing/api/prices/` - List all prices
- `POST /pricing/api/prices/` - Create price
- `POST /pricing/api/prices/{id}/update-selling-price/` - Update selling price
- `GET /pricing/api/pricing-rules/` - List pricing rules
- `GET /pricing/api/special-prices/` - List special prices

**SOAP Endpoint:**
- `POST /pricing/soap/`
- WSDL: `/pricing/soap/?wsdl`

### Returns API

**REST Endpoints:**
- `GET /returns/api/returns/` - List all returns
- `POST /returns/api/returns/` - Create return request
- `POST /returns/api/returns/{return_id}/approve/` - Approve return
- `POST /returns/api/returns/{return_id}/reject/` - Reject return
- `GET /returns/api/replacements/` - List replacements
- `GET /returns/api/refund-transactions/` - List refund transactions

**SOAP Endpoint:**
- `POST /returns/soap/`
- WSDL: `/returns/soap/?wsdl`

### Shipments API

**REST Endpoints:**
- `GET /shipments/api/shipments/` - List all shipments
- `POST /shipments/api/shipments/` - Create shipment
- `GET /shipments/api/shipments/{shipment_id}/track/` - Track shipment
- `POST /shipments/api/shipments/{shipment_id}/dispatch/` - Dispatch shipment
- `POST /shipments/api/shipments/{shipment_id}/deliver/` - Mark as delivered
- `GET /shipments/api/courier-partners/` - List courier partners

**SOAP Endpoint:**
- `POST /shipments/soap/`
- WSDL: `/shipments/soap/?wsdl`

### Reports API

**REST Endpoints:**
- `GET /reports/api/reports/` - List all reports
- `POST /reports/api/reports/` - Generate report
- `GET /reports/api/reports/{report_id}/download/` - Download report
- `POST /reports/api/reports/{report_id}/regenerate/` - Regenerate report
- `GET /reports/api/scheduled-reports/` - List scheduled reports
- `POST /reports/api/scheduled-reports/{schedule_id}/run-now/` - Run report now

**SOAP Endpoint:**
- `POST /reports/soap/`
- WSDL: `/reports/soap/?wsdl`

## Project Structure

```
flipkart-seller-center/
├── flipkart_seller_center/      # Main project settings
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Main URL configuration
│   └── wsgi.py                   # WSGI configuration
├── orders/                       # Orders app
│   ├── models.py                 # Order models
│   ├── serializers.py            # REST serializers
│   ├── views.py                  # REST views
│   ├── soap_views.py             # SOAP views
│   └── urls.py                   # URL routing
├── inventory/                    # Inventory app
│   ├── models.py                 # Product, Inventory, Listing models
│   ├── serializers.py            # REST serializers
│   ├── views.py                  # REST views
│   ├── soap_views.py             # SOAP views
│   └── urls.py                   # URL routing
├── pricing/                      # Pricing app
│   ├── models.py                 # Price, PricingRule models
│   ├── serializers.py            # REST serializers
│   ├── views.py                  # REST views
│   ├── soap_views.py             # SOAP views
│   └── urls.py                   # URL routing
├── returns/                      # Returns app
│   ├── models.py                 # Return, Replacement models
│   ├── serializers.py            # REST serializers
│   ├── views.py                  # REST views
│   ├── soap_views.py             # SOAP views
│   └── urls.py                   # URL routing
├── shipments/                    # Shipments app
│   ├── models.py                 # Shipment, Tracking models
│   ├── serializers.py            # REST serializers
│   ├── views.py                  # REST views
│   ├── soap_views.py             # SOAP views
│   └── urls.py                   # URL routing
├── reports/                      # Reports app
│   ├── models.py                 # Report, ScheduledReport models
│   ├── serializers.py            # REST serializers
│   ├── views.py                  # REST views
│   ├── soap_views.py             # SOAP views
│   └── urls.py                   # URL routing
├── manage.py                     # Django management script
└── requirements.txt              # Python dependencies
```

## Configuration

### Database

The project uses SQLite by default. To use a different database, update the `DATABASES` setting in `flipkart_seller_center/settings.py`.

### API Configuration

Update the Flipkart API credentials in `settings.py`:

```python
FLIPKART_API_CONFIG = {
    'BASE_URL': 'https://api.flipkart.net/sellers',
    'API_KEY': 'your-api-key',
    'API_SECRET': 'your-api-secret',
    'TIMEOUT': 30,
}
```

## Testing SOAP APIs

You can test SOAP APIs using tools like SoapUI or by creating SOAP requests:

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:flip="flipkart.seller.orders">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:get_order>
         <flip:order_id>ORD123456</flip:order_id>
      </flip:get_order>
   </soapenv:Body>
</soapenv:Envelope>
```

## Testing REST APIs

Access the browsable API at each endpoint (e.g., `http://localhost:8000/orders/api/`).

Or use curl:

```bash
# List orders
curl http://localhost:8000/orders/api/orders/

# Get order details
curl http://localhost:8000/orders/api/orders/ORD123456/

# Cancel order
curl -X POST http://localhost:8000/orders/api/orders/ORD123456/cancel/ \
  -H "Content-Type: application/json" \
  -d '{"reason": "Customer request", "cancelled_by": "SELLER"}'
```

## Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to manage all models through a user-friendly interface.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
