# SendPulse API Client

Python client for SendPulse API - email and SMS marketing.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

```python
from client import SendPulseClient

client = SendPulseClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)
```

## API Actions

### Add Email

```python
result = client.add_email(
    books=[12345],
    emails=["john@example.com"]
)
```

### Delete Email

```python
result = client.delete_email("john@example.com", book_id=12345)
```

### Search Contact

```python
result = client.search_contact("john@example.com")
```

### Add Phone Number

```python
result = client.add_phone_number(
    phone="+1234567890",
    book_id=12345,
    variables={"name": "John"}
)
```

### Delete Phone Number

```python
result = client.delete_phone_number("+1234567890", book_id=12345)
```

### Change Phone Number

```python
result = client.change_phone_number(
    phone="+1234567890",
    new_phone="+0987654321",
    book_id=12345
)
```

### Get Phone Number

```python
result = client.get_phone_number("+1234567890", book_id=12345)
```

### Update Variables for Phone

```python
result = client.update_variables_for_phone_number(
    phone="+1234567890",
    book_id=12345,
    variables={"name": "John Updated", "city": "New York"}
)
```

### Add Email to Blacklist

```python
result = client.add_email_to_blacklist("spam@example.com", reason="User request")
```

### Add Phone to Blacklist

```python
result = client.add_phone_number_to_blacklist("+1234567890")
```

### Unsubscribe Mailing List

```python
result = client.unsubscribe_mailing_list(
    emails=["john@example.com"],
    book_id=12345
)
```

### Get Campaign Statistics

```python
result = client.get_email_campaign_statistics(campaign_id=67890)
```

## License

MIT License
