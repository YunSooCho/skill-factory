# DeepL API Client

Python async client for DeepL's translation API.

## Features

- ✅ Translate text to multiple languages
- ✅ Translate documents (PDF, DOCX, PPTX, TXT)
- ✅ Check translation status
- ✅ Download translated documents
- ✅ Auto-detect source language
- ✅ Formality control
- ✅ Async/await support
- ✅ Type hints and dataclasses

## Installation

```bash
pip install -r requirements.txt
```

## API Key

Get your API key from: https://www.deepl.com/pro-api

### Free vs Paid Tier

- **Free Tier**: Uses `api-free.deepl.com` (limited characters)
- **Paid Tier**: Uses `api.deepl.com` (no character limit)

```python
client = DeepLAPIClient(api_key, use_free_tier=True)  # Free tier
# or
client = DeepLAPIClient(api_key, use_free_tier=False)  # Paid tier
```

## Usage

### Translate Text

```python
import asyncio
from deepl_client import DeepLAPIClient

async def main():
    api_key = "your-api-key-here"

    async with DeepLAPIClient(api_key, use_free_tier=True) as client:
        result = await client.translate_text(
            text="Hello, how are you?",
            target_lang="KO",  # Korean
            source_lang="EN",  # English (optional)
            formality="default"  # default, more, less
        )

        translation = result.translations[0]
        print(f"Translated text: {translation.text}")
        print(f"Detected source: {translation.detected_source_language}")

asyncio.run(main())
```

### Translate Document

```python
async with DeepLAPIClient(api_key) as client:
    # Upload document for translation
    result = await client.translate_document(
        file_path="document.pdf",
        target_lang="DE",  # German
        source_lang="EN",  # Optional
        formality="default"
    )

    print(f"Document ID: {result.document_id}")
    print(f"Status: {result.status}")

    # Check translation status
    status = await client.get_translation_status(result.document_id)
    print(f"Translation status: {status.status}")

    if status.status == "done":
        # Download translated document
        await client.download_translated_document(
            document_id=result.document_id,
            output_path="translated.pdf"
        )
        print("Document downloaded successfully!")
```

### Monitor Translation Progress

```python
import asyncio

async def monitor_translation(client, document_id, output_path):
    while True:
        status = await client.get_translation_status(document_id)

        if status.status == "done":
            await client.download_translated_document(document_id, output_path)
            print(f"Translation complete! Saved to {output_path}")
            break
        elif status.status == "translating":
            print(f"Translating... {status.seconds_remaining} seconds remaining")
            await asyncio.sleep(2)
        elif status.status == "error":
            print(f"Error: {status.error_message}")
            break
        else:
            await asyncio.sleep(2)

# Usage:
# await monitor_translation(client, document_id, "output.pdf")
```

## API Actions

### Translate Text

Translate text to target language.

**Parameters:**
- `text` (str): Text to translate
- `target_lang` (str): Target language code (e.g., 'EN', 'DE', 'KO', 'JA')
- `source_lang` (Optional[str]): Source language (auto-detected if not provided)
- `formality` (str): Formality level ('default', 'more', 'less')
- `preserve_formatting` (bool): Preserve formatting (default: False)

**Returns:** `TranslateResponse`

### Translate Document

Upload a document for translation.

**Parameters:**
- `file_path` (str): Path to document file (PDF, DOCX, PPTX, TXT)
- `target_lang` (str): Target language code
- `source_lang` (Optional[str]): Source language code
- `formality` (str): Formality level

**Returns:** `DocumentUploadResponse`

### Get Translation Status

Check the status of a document translation.

**Parameters:**
- `document_id` (str): Document ID from translation request

**Returns:** `DocumentTranslation`

## Supported Language Codes

| Language | Code | Translation | Formalities |
|----------|------|-------------|-------------|
| English | EN | ✅ | default, more, less |
| German | DE | ✅ | default, more, less |
| French | FR | ✅ | default, more, less |
| Spanish | ES | ✅ | default, more, less |
| Italian | IT | ✅ | default, more, less |
| Portuguese | PT | ✅ | default, more, less |
| Dutch | NL | ✅ | default, more, less |
| Polish | PL | ✅ | default, more, less |
| Russian | RU | ✅ | default |
| Japanese | JA | ✅ | default |
| Chinese (Simplified) | ZH | ✅ | default |
| Korean | KO | ✅ | default |

## Document Formats

**Supported input formats:**
- PDF (.pdf)
- Microsoft Word (.docx)
- Microsoft PowerPoint (.pptx)
- Text (.txt)

**Output format:** Same as input format

## API Reference

Official documentation: https://www.deepl.com/docs-api/

## Rate Limits

Check your account limits on the DeepL dashboard:
- Free tier: 500,000 characters/month
- Paid tier: Based on subscription plan

## Support

For issues, visit: https://www.deepl.com/contact