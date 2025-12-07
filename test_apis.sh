#!/bin/bash

# Test script for Flipkart Seller Center APIs
# This script tests both REST and SOAP endpoints

echo "================================================"
echo "Flipkart Seller Center API - Test Script"
echo "================================================"
echo ""

BASE_URL="http://localhost:8000"

echo "1. Testing Home Endpoint..."
curl -s ${BASE_URL}/ | python -m json.tool | head -20
echo ""

echo "================================================"
echo "2. Testing REST APIs"
echo "================================================"
echo ""

echo "2.1. Orders API - List Orders"
curl -s ${BASE_URL}/orders/api/orders/ | python -m json.tool | head -30
echo ""

echo "2.2. Inventory API - List Products"
curl -s ${BASE_URL}/inventory/api/products/ | python -m json.tool | head -30
echo ""

echo "2.3. Pricing API - List Prices"
curl -s ${BASE_URL}/pricing/api/prices/ | python -m json.tool | head -30
echo ""

echo "2.4. Shipments API - List Shipments"
curl -s ${BASE_URL}/shipments/api/shipments/ | python -m json.tool | head -30
echo ""

echo "2.5. Reports API - List Reports"
curl -s ${BASE_URL}/reports/api/reports/ | python -m json.tool | head -30
echo ""

echo "================================================"
echo "3. Testing SOAP APIs"
echo "================================================"
echo ""

echo "3.1. Orders SOAP - Get Order"
cat > /tmp/soap_order_test.xml << 'EOF'
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:flip="flipkart.seller.orders">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:get_order>
         <flip:order_id>ORD-10001</flip:order_id>
      </flip:get_order>
   </soapenv:Body>
</soapenv:Envelope>
EOF
curl -s -X POST -H "Content-Type: text/xml" -d @/tmp/soap_order_test.xml ${BASE_URL}/orders/soap/
echo ""
echo ""

echo "3.2. Inventory SOAP - Get Product"
cat > /tmp/soap_inventory_test.xml << 'EOF'
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:flip="flipkart.seller.inventory">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:get_product>
         <flip:sku>SKU-1001</flip:sku>
      </flip:get_product>
   </soapenv:Body>
</soapenv:Envelope>
EOF
curl -s -X POST -H "Content-Type: text/xml" -d @/tmp/soap_inventory_test.xml ${BASE_URL}/inventory/soap/
echo ""
echo ""

echo "3.3. Shipments SOAP - Get Shipment"
cat > /tmp/soap_shipment_test.xml << 'EOF'
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:flip="flipkart.seller.shipments">
   <soapenv:Header/>
   <soapenv:Body>
      <flip:get_shipment>
         <flip:shipment_id>SHIP-20001</flip:shipment_id>
      </flip:get_shipment>
   </soapenv:Body>
</soapenv:Envelope>
EOF
curl -s -X POST -H "Content-Type: text/xml" -d @/tmp/soap_shipment_test.xml ${BASE_URL}/shipments/soap/
echo ""
echo ""

echo "================================================"
echo "4. Testing WSDL Endpoints"
echo "================================================"
echo ""

echo "4.1. Orders WSDL"
curl -s "${BASE_URL}/orders/soap/?wsdl" | head -10
echo "..."
echo ""

echo "4.2. Inventory WSDL"
curl -s "${BASE_URL}/inventory/soap/?wsdl" | head -10
echo "..."
echo ""

echo "================================================"
echo "All API tests completed!"
echo "================================================"
echo ""
echo "To run this script:"
echo "1. Start the server: python manage.py runserver"
echo "2. Run this script: bash test_apis.sh"
echo ""
