# Amazon Client (MWS / SP-API)

A Python client for Amazon Marketplace Web Services (MWS) and Selling Partner API (SP-API), providing access to orders, inventory, products, reports, and more.

## Features

- **Orders**: List orders, get order details, retrieve order items
- **Inventory**: Check stock levels for SKUs
- **Products**: Get product information for ASINs, SKUs, UPCs
- **Reports**: Request and download various reports
- **Feeds**: Submit bulk operation feeds
- **Financials**: Retrieve financial event data

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

### Getting API Credentials

#### For MWS (Marketplace Web Services):

1. Log into [Amazon Seller Central](https://sellercentral.amazon.com/)
2. Go to **Settings → User Permissions**
3. Click **Visit Seller Central services**
4. Register as a developer
5. Create MWS authorization
6. Note your:
   - **Seller ID** (Merchant ID)
   - **AWS Access Key ID**
   - **Secret Key**
   - **Marketplace ID** (e.g., ATVPDKIKX0DER for US)

#### For SP-API (Selling Partner API):

1. Go to [Amazon Developer Console](https://developer.amazonservices.com/)
2. Create an app
3. Configure security profile
4. Get LWA (Login with Amazon) client credentials
5. Generate refresh token
6. Exchange for access token

### Environment Variables

```bash
# For MWS
export AMAZON_SELLER_ID="A1XXXXX"
export AMAZON_ACCESS_KEY="AKIAIOSFODNN7EXAMPLE"
export AMAZON_SECRET_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AMAZON_MARKETPLACE_ID="ATVPDKIKX0DER"  # US marketplace

# For SP-API (optional)
export AMAZON_SP_API_TOKEN="your_sp_api_access_token"
```

## Usage Example

```python
from amazon import AmazonClient

# Initialize client for a specific region
client = AmazonClient(
    seller_id="A1XXXXX",
    access_key="AKIAIOSFODNN7EXAMPLE",
    secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    marketplace_id="ATVPDKIKX0DER",
    region="US"
)

# List orders
orders = client.list_orders(
    created_after="2024-01-01T00:00:00Z",
    created_before="2024-01-31T23:59:59Z",
    order_statuses=["Unshipped", "PartiallyShipped"]
)

# Get specific order
order = client.get_order("123-1234567-1234567")

# List order items
items = client.list_order_items("123-1234567-1234567")

# List inventory supply for SKUs
inventory = client.list_inventory_supply(
    marketplace_id="ATVPDKIKX0DER",
    merchant_skus=["SKU001", "SKU002"],
    response_group="Detail"
)

# Get product information for ASINs
products = client.get_matching_product_for_id(
    marketplace_id="ATVPDKIKX0DER",
    id_type="ASIN",
    id_list=["B08N5KWB9H", "B08N5KWB9H"]
)

# Get product for SellerSKU
sku_products = client.get_matching_product_for_id(
    marketplace_id="ATVPDKIKX0DER",
    id_type="SellerSKU",
    id_list=["MYSKU001"]
)

# Get category for SKU
categories = client.get_product_categories_for_sku(
    marketplace_id="ATVPDKIKX0DER",
    seller_sku="MYSKU001"
)

# Request a report
report_request = client.request_report(
    report_type="_GET_MERCHANT_LISTINGS_DATA_",
    marketplace_id="ATVPDKIKX0DER",
    start_date="2024-01-01T00:00:00Z",
    end_date="2024-01-31T23:59:59Z"
)

# Get report list
reports = client.get_report_list()

# Get report content
report_content = client.get_report(report_id="123456789")

# Submit feed (XML)
feed_xml = """<?xml version="1.0"?>
<AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
  <Header>
    <DocumentVersion>1.01</DocumentVersion>
    <MerchantIdentifier>M_SELLER_ID</MerchantIdentifier>
  </Header>
  <MessageType>Product</MessageType>
  <PurgeAndReplace>false</PurgeAndReplace>
  <Message>
    <MessageID>1</MessageID>
    <OperationType>Update</OperationType>
    <Product>
      <SKU>MYSKU001</SKU>
      <StandardProductID>
        <Type>ASIN</Type>
        <Value>B08N5KWB9H</Value>
      </StandardProductID>
      <DescriptionData>
        <Title>My Product</Title>
        <Brand>MyBrand</Brand>
      </DescriptionData>
    </Product>
  </Message>
</AmazonEnvelope>"""

feed_result = client.submit_feed(
    feed_type="_POST_PRODUCT_DATA_",
    feed_content=feed_xml,
    marketplace_id="ATVPDKIKX0DER"
)

# Get feed submission status
feed_status = client.get_feed_submission_list()

# List financial events
financials = client.list_financial_events(
    posted_after="2024-01-01T00:00:00Z",
    posted_before="2024-01-31T23:59:59Z",
    max_results=100
)

# Using SP-API (if token is configured)
sp_orders = client.get_orders_sp(
    created_after="2024-01-01T10:00:00Z",
    marketplace_ids=["ATVPDKIKX0DER"],
    order_statuses=["Shipped"]
)
```

## Marketplace IDs

| Marketplace | ID | Region |
|------------|-----|-----------|
| US | ATVPDKIKX0DER | US |
| Canada | A2EUQ1WTGCTBG2 | US |
| Mexico | A1AM78C64UMO4E | US |
| UK | A1F83G8C2ARO7P | EU |
| Germany | A1PA6795UKMFR9 | EU |
| France | A13V1IB3VIYIZH | EU |
| Italy | APJ6JRA9NG5V4 | EU |
| Spain | A1RKKUPIHCS9HS | EU |
| Japan | A1VC38T7YXB5Y6 | FE |

## Report Types

Common report types include:

- `_GET_MERCHANT_LISTINGS_DATA_` - Active listings
- `_GET_FLAT_FILE_OPEN_LISTINGS_DATA_` - Open listings
- `_GET_ORDERS_DATA_` - Order reports
- `_GET_FBA_INVENTORY_DATA_` - FBA inventory
- `_GET_FBA_RECOMMENDATIONS_DATA_` - FBA recommendations
- `_GET_V2_SELLER_PERFORMANCE_DATA_` - Performance metrics

See MWS documentation for complete list.

## Feed Types

Common feed types include:

- `_POST_PRODUCT_DATA_` - Product updates
- `_POST_PRODUCT_PRICING_DATA_` - Price updates
- `_POST_PRODUCT_IMAGE_DATA_` - Image uploads
- `_POST_INVENTORY_AVAILABILITY_DATA_` - Inventory updates
- `_POST_ORDER_ACKNOWLEDGEMENT_DATA_` - Order acknowledgments

## API Documentation

- **MWS**: https://developer.amazonservices.com/
- **SP-API**: https://developer.amazon.com/docs/sp-api

### Key Endpoints

| Resource | Methods |
|----------|---------|
| Orders | list_orders, get_order, list_order_items |
| Inventory | list_inventory_supply |
| Products | get_matching_product_for_id, get_product_categories_for_sku |
| Reports | request_report, get_report_list, get_report |
| Feeds | submit_feed, get_feed_submission_list |
| Financials | list_financial_events |

## Notes

- AWS signature v2 is used for MWS requests
- All dates should be in ISO 8601 format
- Maximum results per request is 100 (MWS)
- Rate limits apply - implement throttling as needed
- MWS is being phased out in favor of SP-API
- Consider using SP-API for new integrations

## Requirements

- Python 3.7+
- requests>=2.31.0

## License

MIT License