"""
API Documentation for Flipkart Seller Center

This document provides detailed information about all available REST and SOAP endpoints.
"""

API_DOCUMENTATION = {
    "orders": {
        "description": "Manage orders, cancellations, and order items",
        "rest_endpoints": [
            {
                "method": "GET",
                "path": "/orders/api/orders/",
                "description": "List all orders",
                "parameters": [],
                "returns": "List of orders with items and cancellations"
            },
            {
                "method": "POST",
                "path": "/orders/api/orders/",
                "description": "Create a new order",
                "body": {
                    "order_id": "string (required)",
                    "order_date": "datetime (required)",
                    "status": "string (required)",
                    "customer_name": "string (required)",
                    "total_amount": "decimal (required)",
                    "payment_method": "string (required)",
                    "shipping_address": "string (required)"
                },
                "returns": "Created order details"
            },
            {
                "method": "GET",
                "path": "/orders/api/orders/{order_id}/",
                "description": "Get order details",
                "parameters": ["order_id"],
                "returns": "Order details with items and cancellations"
            },
            {
                "method": "POST",
                "path": "/orders/api/orders/{order_id}/cancel/",
                "description": "Cancel an order",
                "body": {
                    "reason": "string (required)",
                    "cancelled_by": "string (SELLER/CUSTOMER)",
                    "refund_amount": "decimal"
                },
                "returns": "Cancellation confirmation"
            },
            {
                "method": "POST",
                "path": "/orders/api/orders/{order_id}/dispatch/",
                "description": "Mark order as ready to dispatch",
                "returns": "Dispatch confirmation"
            },
            {
                "method": "GET",
                "path": "/orders/api/orders/{order_id}/track/",
                "description": "Track order status",
                "returns": "Order tracking information"
            }
        ],
        "soap_operations": [
            {
                "operation": "get_order",
                "parameters": ["order_id"],
                "description": "Get order details by order ID"
            },
            {
                "operation": "list_orders",
                "parameters": [],
                "description": "List all orders"
            },
            {
                "operation": "cancel_order",
                "parameters": ["order_id", "reason", "cancelled_by"],
                "description": "Cancel an order"
            },
            {
                "operation": "dispatch_order",
                "parameters": ["order_id"],
                "description": "Mark order as ready to dispatch"
            },
            {
                "operation": "track_order",
                "parameters": ["order_id"],
                "description": "Track order status"
            }
        ]
    },
    
    "inventory": {
        "description": "Manage products, inventory, and listings",
        "rest_endpoints": [
            {
                "method": "GET",
                "path": "/inventory/api/products/",
                "description": "List all products",
                "returns": "List of products with inventory and listings"
            },
            {
                "method": "POST",
                "path": "/inventory/api/products/",
                "description": "Create a new product",
                "body": {
                    "sku": "string (required)",
                    "fsn": "string (required)",
                    "product_name": "string (required)",
                    "brand": "string (required)",
                    "category": "string (required)",
                    "mrp": "decimal (required)",
                    "hsn_code": "string (required)",
                    "tax_percentage": "decimal (required)"
                },
                "returns": "Created product details"
            },
            {
                "method": "POST",
                "path": "/inventory/api/products/{sku}/activate/",
                "description": "Activate a product",
                "returns": "Activation confirmation"
            },
            {
                "method": "POST",
                "path": "/inventory/api/products/{sku}/deactivate/",
                "description": "Deactivate a product",
                "returns": "Deactivation confirmation"
            },
            {
                "method": "GET",
                "path": "/inventory/api/inventory/",
                "description": "List all inventory records",
                "returns": "List of inventory with stock levels"
            },
            {
                "method": "POST",
                "path": "/inventory/api/inventory/{id}/update-stock/",
                "description": "Update stock levels",
                "body": {
                    "available_quantity": "integer",
                    "reserved_quantity": "integer",
                    "damaged_quantity": "integer"
                },
                "returns": "Updated inventory details"
            }
        ],
        "soap_operations": [
            {
                "operation": "get_product",
                "parameters": ["sku"],
                "description": "Get product details by SKU"
            },
            {
                "operation": "list_products",
                "parameters": [],
                "description": "List all active products"
            },
            {
                "operation": "get_inventory",
                "parameters": ["sku"],
                "description": "Get inventory details by product SKU"
            },
            {
                "operation": "update_stock",
                "parameters": ["sku", "available_quantity"],
                "description": "Update stock levels for a product"
            },
            {
                "operation": "activate_product",
                "parameters": ["sku"],
                "description": "Activate a product"
            },
            {
                "operation": "deactivate_product",
                "parameters": ["sku"],
                "description": "Deactivate a product"
            }
        ]
    },
    
    "pricing": {
        "description": "Manage pricing, special prices, and pricing rules",
        "rest_endpoints": [
            {
                "method": "GET",
                "path": "/pricing/api/prices/",
                "description": "List all prices",
                "returns": "List of prices with profit margins"
            },
            {
                "method": "POST",
                "path": "/pricing/api/prices/{id}/update-selling-price/",
                "description": "Update selling price",
                "body": {
                    "selling_price": "decimal (required)"
                },
                "returns": "Updated price details"
            },
            {
                "method": "GET",
                "path": "/pricing/api/special-prices/",
                "description": "List all special prices/promotions",
                "returns": "List of special prices"
            },
            {
                "method": "GET",
                "path": "/pricing/api/pricing-rules/",
                "description": "List all pricing rules",
                "returns": "List of pricing rules"
            }
        ],
        "soap_operations": [
            {
                "operation": "get_price",
                "parameters": ["sku"],
                "description": "Get price details for a product"
            },
            {
                "operation": "update_selling_price",
                "parameters": ["sku", "new_price"],
                "description": "Update selling price for a product"
            },
            {
                "operation": "get_profit_margin",
                "parameters": ["sku"],
                "description": "Calculate profit margin for a product"
            },
            {
                "operation": "list_special_prices",
                "parameters": ["sku"],
                "description": "List all special prices for a product"
            }
        ]
    },
    
    "returns": {
        "description": "Handle returns, replacements, and refunds",
        "rest_endpoints": [
            {
                "method": "GET",
                "path": "/returns/api/returns/",
                "description": "List all returns",
                "returns": "List of return requests"
            },
            {
                "method": "POST",
                "path": "/returns/api/returns/{return_id}/approve/",
                "description": "Approve a return request",
                "returns": "Approval confirmation"
            },
            {
                "method": "POST",
                "path": "/returns/api/returns/{return_id}/reject/",
                "description": "Reject a return request",
                "returns": "Rejection confirmation"
            },
            {
                "method": "GET",
                "path": "/returns/api/replacements/",
                "description": "List all replacements",
                "returns": "List of replacements"
            },
            {
                "method": "POST",
                "path": "/returns/api/replacements/{replacement_id}/dispatch/",
                "description": "Dispatch a replacement",
                "body": {
                    "tracking_id": "string"
                },
                "returns": "Dispatch confirmation"
            },
            {
                "method": "GET",
                "path": "/returns/api/refund-transactions/",
                "description": "List all refund transactions",
                "returns": "List of refund transactions"
            }
        ],
        "soap_operations": [
            {
                "operation": "get_return",
                "parameters": ["return_id"],
                "description": "Get return details by return ID"
            },
            {
                "operation": "list_returns",
                "parameters": [],
                "description": "List all returns"
            },
            {
                "operation": "approve_return",
                "parameters": ["return_id"],
                "description": "Approve a return request"
            },
            {
                "operation": "reject_return",
                "parameters": ["return_id"],
                "description": "Reject a return request"
            },
            {
                "operation": "get_replacement",
                "parameters": ["replacement_id"],
                "description": "Get replacement details"
            },
            {
                "operation": "dispatch_replacement",
                "parameters": ["replacement_id", "tracking_id"],
                "description": "Dispatch a replacement"
            },
            {
                "operation": "get_refund_status",
                "parameters": ["transaction_id"],
                "description": "Get refund transaction status"
            }
        ]
    },
    
    "shipments": {
        "description": "Manage shipments, tracking, and courier partners",
        "rest_endpoints": [
            {
                "method": "GET",
                "path": "/shipments/api/shipments/",
                "description": "List all shipments",
                "returns": "List of shipments with tracking"
            },
            {
                "method": "GET",
                "path": "/shipments/api/shipments/{shipment_id}/track/",
                "description": "Track shipment",
                "returns": "Shipment tracking information"
            },
            {
                "method": "POST",
                "path": "/shipments/api/shipments/{shipment_id}/dispatch/",
                "description": "Dispatch a shipment",
                "body": {
                    "location": "string"
                },
                "returns": "Dispatch confirmation"
            },
            {
                "method": "POST",
                "path": "/shipments/api/shipments/{shipment_id}/deliver/",
                "description": "Mark shipment as delivered",
                "body": {
                    "location": "string"
                },
                "returns": "Delivery confirmation"
            },
            {
                "method": "GET",
                "path": "/shipments/api/courier-partners/",
                "description": "List all courier partners",
                "returns": "List of courier partners"
            }
        ],
        "soap_operations": [
            {
                "operation": "get_shipment",
                "parameters": ["shipment_id"],
                "description": "Get shipment details by shipment ID"
            },
            {
                "operation": "track_shipment",
                "parameters": ["tracking_number"],
                "description": "Track shipment by tracking number"
            },
            {
                "operation": "dispatch_shipment",
                "parameters": ["shipment_id"],
                "description": "Dispatch a shipment"
            },
            {
                "operation": "deliver_shipment",
                "parameters": ["shipment_id"],
                "description": "Mark shipment as delivered"
            },
            {
                "operation": "list_courier_partners",
                "parameters": [],
                "description": "List all active courier partners"
            },
            {
                "operation": "get_courier_partner",
                "parameters": ["partner_code"],
                "description": "Get courier partner details"
            }
        ]
    },
    
    "reports": {
        "description": "Generate and download reports",
        "rest_endpoints": [
            {
                "method": "GET",
                "path": "/reports/api/reports/",
                "description": "List all reports",
                "returns": "List of generated reports"
            },
            {
                "method": "POST",
                "path": "/reports/api/reports/",
                "description": "Generate a new report",
                "body": {
                    "report_type": "string (SALES/ORDERS/INVENTORY/RETURNS/SHIPMENTS/FINANCIAL/PERFORMANCE)",
                    "report_name": "string",
                    "report_format": "string (CSV/XLSX/PDF/JSON)",
                    "start_date": "date",
                    "end_date": "date",
                    "requested_by": "string"
                },
                "returns": "Report generation confirmation"
            },
            {
                "method": "GET",
                "path": "/reports/api/reports/{report_id}/download/",
                "description": "Download a report",
                "returns": "Report download URL"
            },
            {
                "method": "POST",
                "path": "/reports/api/reports/{report_id}/regenerate/",
                "description": "Regenerate a report",
                "returns": "Regeneration confirmation"
            },
            {
                "method": "GET",
                "path": "/reports/api/scheduled-reports/",
                "description": "List all scheduled reports",
                "returns": "List of scheduled reports"
            },
            {
                "method": "POST",
                "path": "/reports/api/scheduled-reports/{schedule_id}/run-now/",
                "description": "Run scheduled report immediately",
                "returns": "Execution confirmation"
            }
        ],
        "soap_operations": [
            {
                "operation": "get_report",
                "parameters": ["report_id"],
                "description": "Get report details by report ID"
            },
            {
                "operation": "get_report_status",
                "parameters": ["report_id"],
                "description": "Get report generation status"
            },
            {
                "operation": "download_report",
                "parameters": ["report_id"],
                "description": "Get report download URL"
            },
            {
                "operation": "generate_report",
                "parameters": ["report_type", "report_format", "requested_by"],
                "description": "Generate a new report"
            },
            {
                "operation": "list_scheduled_reports",
                "parameters": [],
                "description": "List all active scheduled reports"
            },
            {
                "operation": "get_scheduled_report",
                "parameters": ["schedule_id"],
                "description": "Get scheduled report details"
            },
            {
                "operation": "run_scheduled_report",
                "parameters": ["schedule_id"],
                "description": "Run a scheduled report immediately"
            }
        ]
    }
}
