"""
Pappers API - French Company Information Client

Supports company search, retrieval, and document downloads.

API Actions (3):
1. Search Company
2. Get Company
3. Download Document
"""

import aiohttp
import asyncio
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class Company:
    """Company data model"""
    siret: Optional[str] = None
    siren: Optional[str] = None
    nom_entreprise: str = ""
    nom_complet: Optional[str] = None
    siege: Dict[str, Any] = field(default_factory=dict)
    etablissements: List[Dict[str, Any]] = field(default_factory=list)
    dirigeants: List[Dict[str, Any]] = field(default_factory=list)
    date_creation: Optional[str] = None
    date_radiation: Optional[str] = None
    statut: str = ""
    code_postal: Optional[str] = None
    ville: Optional[str] = None
    region: Optional[str] = None
    pays: Optional[str] = None
    activite_principale: Optional[str] = None
    capital: Optional[float] = None
    forme_juridique: Optional[str] = None
    documents: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SearchResult:
    """Search result data model"""
    results: List[Company] = field(default_factory=list)
    total: int = 0
    page: int = 1
    per_page: int = 20


class PappersClient:
    """
    Pappers API client for French company information.

    API Documentation: https://www.pappers.fr/api/
    Authentication: API Key via header
    Protocol: HTTPS REST API
    """

    BASE_URL = "https://api.pappers.fr/v2"
    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 0.5  # seconds between requests

    def __init__(self, api_key: str):
        """Initialize Pappers client"""
        self.api_key = api_key
        self.session = None
        self._last_request_time = 0

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _rate_limit(self):
        """Simple rate limiting"""
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self.RATE_LIMIT_DELAY:
            await asyncio.sleep(self.RATE_LIMIT_DELAY - time_since_last_request)
        self._last_request_time = time.time()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make API request with retry logic and error handling"""
        await self._rate_limit()

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        url = f"{self.BASE_URL}{endpoint}"

        for attempt in range(self.MAX_RETRIES):
            try:
                async with self.session.request(
                    method,
                    url,
                    params=params,
                    json=json_data,
                    headers=headers
                ) as response:
                    if response.status == 204:
                        return {}

                    data = await response.json()

                    if response.status in (200, 201, 204):
                        return data
                    elif response.status == 401:
                        raise Exception("Invalid API key or unauthorized access")
                    elif response.status == 403:
                        raise Exception("Insufficient permissions")
                    elif response.status == 404:
                        raise Exception("Company or resource not found")
                    elif response.status == 429:
                        retry_after = int(response.headers.get("Retry-After", 5))
                        await asyncio.sleep(retry_after)
                        continue
                    elif 400 <= response.status < 500:
                        raise Exception(f"Client error: {data.get('message', data.get('error', 'Unknown error'))}")
                    else:
                        raise Exception(f"Server error: {response.status} - {data}")

            except aiohttp.ClientError as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise Exception(f"Request failed after {self.MAX_RETRIES} attempts: {str(e)}")
                await asyncio.sleep(2 ** attempt)

    # ==================== Company Operations ====================

    async def search_company(
        self,
        query: str,
        page: int = 1,
        per_page: int = 20,
        code_postal: Optional[str] = None,
        departement: Optional[str] = None,
        region: Optional[str] = None
    ) -> SearchResult:
        """
        Search for companies (Search Company)

        Args:
            query: Search query (company name, SIRET/SIREN, etc.)
            page: Page number (default: 1)
            per_page: Results per page (default: 20, max: 100)
            code_postal: Filter by postal code
            departement: Filter by department
            region: Filter by region

        Returns:
            SearchResult with list of companies
        """
        params = {
            "q": query,
            "page": page,
            "par_page": per_page
        }

        if code_postal:
            params["code_postal"] = code_postal
        if departement:
            params["departement"] = departement
        if region:
            params["region"] = region

        response = await self._request("GET", "/recherche", params=params)

        results = response.get("resultats", [])
        companies = [Company(**self._map_company_data(c)) for c in results]

        return SearchResult(
            results=companies,
            total=response.get("total", 0),
            page=page,
            per_page=per_page
        )

    async def get_company(self, siret: str) -> Company:
        """
        Get company by SIRET (Get Company)

        Args:
            siret: Company SIRET number (14 digits)

        Returns:
            Company with detailed information
        """
        params = {"siret": siret}
        response = await self._request("GET", "/entreprise", params=params)

        return Company(**self._map_company_data(response))

    def _map_company_data(self, data: Dict) -> Dict:
        """Map Pappers company data to our Company model"""
        siege = data.get("siege", {})
        return {
            "siret": data.get("siret"),
            "siren": data.get("siren"),
            "nom_entreprise": data.get("nom_entreprise", ""),
            "nom_complet": data.get("nom_entreprise"),
            "siege": siege,
            "etablissements": data.get("etablissements", []),
            "dirigeants": data.get("dirigeants", []),
            "date_creation": data.get("date_creation"),
            "date_radiation": data.get("date_radiation"),
            "statut": data.get("statut_radiation", "ouverte"),
            "code_postal": siege.get("code_postal"),
            "ville": siege.get("ville"),
            "region": siege.get("region"),
            "pays": siege.get("pays"),
            "activite_principale": siege.get("activite_principale"),
            "capital": data.get("capital"),
            "forme_juridique": data.get("forme_juridique"),
            "documents": data.get("documents", [])
        }

    # ==================== Document Operations ====================

    async def download_document(
        self,
        siret: str,
        document_type: str = "statuts"
    ) -> bytes:
        """
        Download document for a company (Download Document)

        Args:
            siret: Company SIRET number
            document_type: Type of document (statuts, kbis, etc.)

        Returns:
            Document content as bytes

        Raises:
            Exception: If document cannot be fetched
        """
        params = {
            "siret": siret,
            "type": document_type
        }

        await self._rate_limit()

        headers = {
            "x-api-key": self.api_key,
            "Accept": "application/pdf"
        }

        url = f"{self.BASE_URL}/document"

        for attempt in range(self.MAX_RETRIES):
            try:
                async with self.session.get(
                    url,
                    params=params,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        return await response.read()
                    elif response.status == 401:
                        raise Exception("Invalid API key")
                    elif response.status == 404:
                        raise Exception("Document not found")
                    elif response.status == 429:
                        retry_after = int(response.headers.get("Retry-After", 5))
                        await asyncio.sleep(retry_after)
                        continue
                    else:
                        raise Exception(f"Error downloading document: {response.status}")

            except aiohttp.ClientError as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise Exception(f"Request failed after {self.MAX_RETRIES} attempts: {str(e)}")
                await asyncio.sleep(2 ** attempt)

        raise Exception("Failed to download document")


# ==================== Example Usage ====================

async def main():
    """Example usage of Pappers client"""

    api_key = "your_pappers_api_key"

    async with PappersClient(api_key=api_key) as client:
        # Search for companies
        search_query = "Google France"
        results = await client.search_company(search_query, per_page=5)

        print(f"Found {results.total} companies matching '{search_query}'")
        for company in results.results[:3]:
            print(f"  - {company.nom_entreprise} (SIRET: {company.siret})")

        # Get company details
        if results.results:
            siret = results.results[0].siret
            if siret:
                company = await client.get_company(siret)
                print(f"\nCompany details for {company.nom_entreprise}:")
                print(f"  Address: {company.siege.get('adresse_ligne_1', '')}")
                print(f"  City: {company.siege.get('ville', '')}")
                print(f"  Activity: {company.activite_principale}")

                # Download document (e.g., articles of incorporation)
                # document_bytes = await client.download_document(siret, "statuts")
                # with open(f"{siret}.pdf", 'wb') as f:
                #     f.write(document_bytes)


async def search_by_siret():
    """Example: Search by SIRET"""
    api_key = "your_pappers_api_key"

    async with PappersClient(api_key=api_key) as client:
        # Get company by SIRET directly
        siret = "44306184100030"  # Example SIRET
        try:
            company = await client.get_company(siret)
            print(f"Company: {company.nom_entreprise}")
            print(f"Status: {company.statut}")
            print(f"Capital: {company.capital}€")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(search_by_siret())