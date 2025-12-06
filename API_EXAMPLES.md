# API Usage Examples

This document provides practical examples for using the Flipkart Seller Center APIs.

## Setup

1. Start the Django development server:
```bash
python manage.py runserver
```

2. Optionally populate sample data:
```bash
python manage.py populate_sample_data
```

## REST API Examples

### Orders API

#### List all orders
```bash
curl http://localhost:8000/orders/api/orders/
```

#### Get specific order
```bash
curl http://localhost:8000/orders/api/orders/ORD-10001/
```

#### Create a new order
```bash
curl -X POST http://localhost:8000/orders/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ORD-12345",
    "order_date": "2025-12-06T10:00:00Z",
    "status": "APPROVED",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_phone": "9876543210",
    "shipping_address": "123 Main St, City",
    "billing_address": "123 Main St, City",
    "total_amount": 5000.00,
    "payment_method": "UPI"
  }'
```

#### Cancel an order
```bash
curl -X POST http://localhost:8000/orders/api/orders/ORD-10001/cancel/ \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Customer requested cancellation",
    "cancelled_by": "SELLER",
    "refund_amount": 5000.00
  }'
```

#### Track an order
```bash
curl http://localhost:8000/orders/api/orders/ORD-10001/track/
```

### Inventory API

#### List all products
```bash
curl http://localhost:8000/inventory/api/products/
```

#### Get specific product
```bash
curl http://localhost:8000/inventory/api/products/SKU-1001/
```

#### Create a product
```bash
curl -X POST http://localhost:8000/inventory/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "SKU-9999",
    "fsn": "FSN-9999",
    "product_name": "Test Product",
    "brand": "TestBrand",
    "category": "Electronics",
    "mrp": 1500.00,
    "hsn_code": "HSN1500",
    "tax_percentage": 18.00,
    "is_active": true
  }'
```

#### Update stock levels
```bash
curl -X POST http://localhost:8000/inventory/api/inventory/1/update-stock/ \
  -H "Content-Type: application/json" \
  -d '{
    "available_quantity": 150,
    "reserved_quantity": 15,
    "damaged_quantity": 5
  }'
```

#### Activate/Deactivate product
```bash
# Activate
curl -X POST http://localhost:8000/inventory/api/products/SKU-1001/activate/

# Deactivate
curl -X POST http://localhost:8000/inventory/api/products/SKU-1001/deactivate/
```

### Pricing API

#### List all prices
```bash
curl http://localhost:8000/pricing/api/prices/
```

#### Update selling price
```bash
curl -X POST http://localhost:8000/pricing/api/prices/1/update-selling-price/ \
  -H "Content-Type: application/json" \
  -d '{
    "selling_price": 850.00
  }'
```

#### List special prices
```bash
curl http://localhost:8000/pricing/api/special-prices/
```

### Returns API

#### List all returns
```bash
curl http://localhost:8000/returns/api/returns/
```

#### Approve a return
```bash
curl -X POST http://localhost:8000/returns/api/returns/RET-12345/approve/
```

#### Reject a return
```bash
curl -X POST http://localhost:8000/returns/api/returns/RET-12345/reject/
```

#### Dispatch a replacement
```bash
curl -X POST http://localhost:8000/returns/api/replacements/REPL-12345/dispatch/ \
  -H "Content-Type: application/json" \
  -d '{
    "tracking_id": "TRK-54321"
  }'
```

### Shipments API

#### List all shipments
```bash
curl http://localhost:8000/shipments/api/shipments/
```

#### Track a shipment
```bash
curl http://localhost:8000/shipments/api/shipments/SHIP-20001/track/
```

#### Dispatch a shipment
```bash
curl -X POST http://localhost:8000/shipments/api/shipments/SHIP-20001/dispatch/ \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Mumbai Warehouse"
  }'
```

#### Mark shipment as delivered
```bash
curl -X POST http://localhost:8000/shipments/api/shipments/SHIP-20001/deliver/ \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Customer Address"
  }'
```

#### List courier partners
```bash
curl http://localhost:8000/shipments/api/courier-partners/
```

### Reports API

#### List all reports
```bash
curl http://localhost:8000/reports/api/reports/
```

#### Generate a new report
```bash
curl -X POST http://localhost:8000/reports/api/reports/ \
  -H "Content-Type: application/json" \
  -d '{
    "report_id": "RPT-50001",
    "report_type": "SALES",
    "report_name": "Monthly Sales Report",
    "report_format": "XLSX",
    "start_date": "2025-11-01",
    "end_date": "2025-11-30",
    "requested_by": "Admin"
  }'
```

#### Download a report
```bash
curl http://localhost:8000/reports/api/reports/RPT-40001/download/
```

#### List scheduled reports
```bash
curl http://localhost:8000/reports/api/scheduled-reports/
```

#### Run scheduled report now
```bash
curl -X POST http://localhost:8000/reports/api/scheduled-reports/SCH-50001/run-now/
```

---

## SOAP API Examples

### Orders SOAP API

#### Get Order
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:flip="flipkart.seller.orders">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:get_order>
         <flip:order_id>ORD-10001</flip:order_id>
      </flip:get_order>
   </soapenv:Body>
</soapenv:Envelope>
```

```bash
curl -X POST http://localhost:8000/orders/soap/ \
  -H "Content-Type: text/xml" \
  -d @request.xml
```

#### List Orders
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:flip="flipkart.seller.orders">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:list_orders/>
   </soapenv:Body>
</soapenv:Envelope>
```

#### Cancel Order
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:flip="flipkart.seller.orders">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:cancel_order>
         <flip:order_id>ORD-10001</flip:order_id>
         <flip:reason>Customer request</flip:reason>
         <flip:cancelled_by>SELLER</flip:cancelled_by>
      </flip:cancel_order>
   </soapenv:Body>
</soapenv:Envelope>
```

### Inventory SOAP API

#### Get Product
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:flip="flipkart.seller.inventory">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:get_product>
         <flip:sku>SKU-1001</flip:sku>
      </flip:get_product>
   </soapenv:Body>
</soapenv:Envelope>
```

#### Update Stock
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:flip="flipkart.seller.inventory">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:update_stock>
         <flip:sku>SKU-1001</flip:sku>
         <flip:available_quantity>150</flip:available_quantity>
      </flip:update_stock>
   </soapenv:Body>
</soapenv:Envelope>
```

### Shipments SOAP API

#### Get Shipment
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:flip="flipkart.seller.shipments">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:get_shipment>
         <flip:shipment_id>SHIP-20001</flip:shipment_id>
      </flip:get_shipment>
   </soapenv:Body>
</soapenv:Envelope>
```

#### Track Shipment
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:flip="flipkart.seller.shipments">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:track_shipment>
         <flip:tracking_number>TRK-30001</flip:tracking_number>
      </flip:track_shipment>
   </soapenv:Body>
</soapenv:Envelope>
```

### Reports SOAP API

#### Generate Report
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:flip="flipkart.seller.reports">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:generate_report>
         <flip:report_type>SALES</flip:report_type>
         <flip:report_format>CSV</flip:report_format>
         <flip:requested_by>Admin</flip:requested_by>
      </flip:generate_report>
   </soapenv:Body>
</soapenv:Envelope>
```

#### Get Report Status
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:flip="flipkart.seller.reports">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:get_report_status>
         <flip:report_id>RPT-40001</flip:report_id>
      </flip:get_report_status>
   </soapenv:Body>
</soapenv:Envelope>
```

---

## Using Python Requests Library

### REST API with Python

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

# List products
response = requests.get(f"{BASE_URL}/inventory/api/products/")
products = response.json()
print(json.dumps(products, indent=2))

# Get specific product
response = requests.get(f"{BASE_URL}/inventory/api/products/SKU-1001/")
product = response.json()
print(json.dumps(product, indent=2))

# Create order
order_data = {
    "order_id": "ORD-99999",
    "order_date": "2025-12-06T10:00:00Z",
    "status": "APPROVED",
    "customer_name": "Jane Doe",
    "total_amount": 3000.00,
    "payment_method": "COD",
    "shipping_address": "456 Street, City"
}
response = requests.post(
    f"{BASE_URL}/orders/api/orders/",
    json=order_data
)
print(response.json())

# Update stock
stock_data = {
    "available_quantity": 200
}
response = requests.post(
    f"{BASE_URL}/inventory/api/inventory/1/update-stock/",
    json=stock_data
)
print(response.json())
```

### SOAP API with Python

```python
import requests

# SOAP request
soap_request = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:flip="flipkart.seller.inventory">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:get_product>
         <flip:sku>SKU-1001</flip:sku>
      </flip:get_product>
   </soapenv:Body>
</soapenv:Envelope>
"""

# Make SOAP request
headers = {'Content-Type': 'text/xml'}
response = requests.post(
    'http://localhost:8000/inventory/soap/',
    data=soap_request,
    headers=headers
)

print(response.text)
```

---

## Testing with Postman

1. **Import Collection**: Create a new collection for each app
2. **Set Base URL**: Configure environment variable for `BASE_URL`
3. **Add Requests**: Add GET, POST, PUT, DELETE requests for each endpoint
4. **Test SOAP**: Use "POST" method with XML body for SOAP requests

---

## Browsable API

Django REST Framework provides a browsable API interface. Simply visit any REST endpoint in your browser:

- http://localhost:8000/orders/api/orders/
- http://localhost:8000/inventory/api/products/
- http://localhost:8000/pricing/api/prices/
- etc.

You can interact with the API directly through the web interface!

---

## WSDL Access

Access WSDL definitions for SOAP services:

- Orders: http://localhost:8000/orders/soap/?wsdl
- Inventory: http://localhost:8000/inventory/soap/?wsdl
- Pricing: http://localhost:8000/pricing/soap/?wsdl
- Returns: http://localhost:8000/returns/soap/?wsdl
- Shipments: http://localhost:8000/shipments/soap/?wsdl
- Reports: http://localhost:8000/reports/soap/?wsdl

Use these WSDLs with SOAP client tools like SoapUI, Postman, or programmatic SOAP libraries.
