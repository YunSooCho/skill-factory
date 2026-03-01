# Axonaut API Client

Python client for Axonaut business management API.

## Features

- Companies: Full CRUD operations
- Products: Manage products and pricing
- Invoices & Quotations: Create and manage
- Opportunities: Sales pipeline management
- Employees: Team management
- Expenses: Expense tracking
- Events & Tickets: Event management

## Installation

```bash
pip install aiohttp
```

## API Actions (30)

Full CRUD for companies, contacts, products, invoices, opportunities, employees, expenses

## Triggers (20)

- New Company, Deal, Invoice, Task, Opportunity, etc.
- Updated Company, Deal, Product, Ticket, Employee, Expense, Event, Project

## Usage

```python
import asyncio
from axonaut import AxonautClient

async def main():
    client = AxonautClient(api_key="your_key")

    # Create company
    company = await client.create_company({"name": "Acme Corp"})
    print(f"Created company: {company.id}")

    # Create product
    product = await client.create_product({"name": "Service", "price": 100})
    print(f"Created product: {product.id}")

    # Create opportunity
    opp = await client.create_opportunity({"name": "Big Deal", "company_id": company.id})
    print(f"Created opportunity: {opp.id}")

asyncio.run(main())
```

## Testing

Requires API key test operations.

## Authentication

Get API key from Axonaut dashboard.

## License

MIT