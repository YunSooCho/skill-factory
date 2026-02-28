"""
CNPJA - Brazilian Company Registry API Client

This module provides a Python client for accessing CNPJ information
from the Brazilian National Company Registry.
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class CNPJAClient:
    """
    Client for CNPJA - Brazilian National Company Registry.

    CNPJA provides:
    - Company information by CNPJ number
    - Legal entity details
    - Registration status and history
    - QSA (Qualified Shareholders) information
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://publica.cnpj.ws/cnpj",
        timeout: int = 30
    ):
        """
        Initialize the CNPJA client.

        Args:
            api_key: Optional API key for premium features
            base_url: Base URL for the CNPJA API
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'cnpja-python-client/1.0'
        })

        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'

    def _request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the API."""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(
            url,
            params=params,
            timeout=self.timeout
        )

        if response.status_code == 404:
            raise ValueError(f"CNPJ not found: {endpoint}")
        elif response.status_code == 429:
            raise Exception("Rate limit exceeded. Please try again later.")
        elif response.status_code >= 400:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            raise Exception(f"API error {response.status_code}: {error_data.get('message', response.text)}")

        return response.json()

    def get_company(self, cnpj: str) -> Dict[str, Any]:
        """
        Get company information by CNPJ.

        Args:
            cnpj: CNPJ number (with or without formatting)

        Returns:
            Company information dictionary

        Raises:
            ValueError: If CNPJP is not found
            Exception: For API errors
        """
        # Clean CNPJ - remove dots, slashes, dashes
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')

        if len(cnpj) != 14:
            raise ValueError("Invalid CNPJ: must be 14 digits")

        return self._request(cnpj)

    def get_company_raw(self, cnpj: str) -> Dict[str, Any]:
        """
        Get raw company data without preprocessing.

        Args:
            cnpj: CNPJ number

        Returns:
            Raw company data
        """
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
        return self._request(f"{cnpj}/raw")

    def get_company_history(self, cnpj: str) -> List[Dict[str, Any]]:
        """
        Get company registration history.

        Args:
            cnpj: CNPJ number

        Returns:
            List of historical entries
        """
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
        return self._request(f"{cnpj}/historico")

    def get_company_qsa(self, cnpj: str) -> List[Dict[str, Any]]:
        """
        Get QSA (Qualified Shareholders) information.

        Args:
            cnpj: CNPJ number

        Returns:
            List of QSA entries
        """
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
        return self._request(f"{cnpj}/qsa")

    def get_company_simples(self, cnpj: str) -> Dict[str, Any]:
        """
        Get Simples Nacional information.

        Args:
            cnpj: CNPJ number

        Returns:
            Simples Nacional status and information
        """
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
        return self._request(f"{cnpj}/simples")

    def lookup_company(
        self,
        cnpj: Optional[str] = None,
        name: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Lookup companies by various criteria.

        Args:
            cnpj: CNPJ number (exact match)
            name: Company name (partial match)
            city: City name
            state: State abbreviation (e.g., 'SP')
            limit: Maximum number of results

        Returns:
            List of matching companies

        Note:
            This feature may require premium API key
        """
        params = {}
        if cnpj:
            params['cnpj'] = cnpj.replace('.', '').replace('/', '').replace('-', '')
        if name:
            params['nome'] = name
        if city:
            params['cidade'] = city
        if state:
            params['uf'] = state.upper()
        if limit:
            params['limit'] = limit

        return self._request('buscar', params)

    def get_company_partners(self, cnpj: str) -> List[Dict[str, Any]]:
        """
        Get company partners/socios information.

        Args:
            cnpj: CNPJ number

        Returns:
            List of partner entries
        """
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
        return self._request(f"{cnpj}/socios")

    def get_company_activities(self, cnpj: str) -> Dict[str, Any]:
        """
        Get company economic activities (CNAE).

        Args:
            cnpj: CNPJ number

        Returns:
            Primary and secondary activities
        """
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
        return self._request(f"{cnpj}/cnaes")

    def get_company_contacts(self, cnpj: str) -> Dict[str, Any]:
        """
        Get company contact information.

        Args:
            cnpj: CNPJ number

        Returns:
            Email, phone, and other contact details
        """
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
        return self._request(f"{cnpj}/contato")

    def validate_cnpj(self, cnpj: str) -> bool:
        """
        Validate CNPJ checksum.

        Args:
            cnpj: CNPJ number (with or without formatting)

        Returns:
            True if valid, False otherwise
        """
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')

        if len(cnpj) != 14 or not cnpj.isdigit():
            return False

        # Brazilian CNPJ validation algorithm
        def calculate_digit(cnpj_base: str, weights: List[int]) -> int:
            total = 0
            for i in range(len(cnpj_base)):
                total += int(cnpj_base[i]) * weights[i]
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder

        base = cnpj[:12]
        first_digit = calculate_digit(base, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])

        base_with_first = base + str(first_digit)
        second_digit = calculate_digit(base_with_first, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])

        return cnpj[-2:] == f"{first_digit}{second_digit}"

    def format_cnpj(self, cnpj: str) -> str:
        """
        Format CNPJ with standard separators.

        Args:
            cnpj: CNPJ number (14 digits)

        Returns:
            Formatted CNPJ (XX.XXX.XXX/XXXX-XX)
        """
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')

        if len(cnpj) != 14:
            return cnpj

        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

    def get_company_summary(self, cnpj: str) -> Dict[str, Any]:
        """
        Get a concise company summary.

        Args:
            cnpj: CNPJ number

        Returns:
            Simplified company information suitable for display
        """
        try:
            company = self.get_company(cnpj)

            summary = {
                'cnpj': self.format_cnpj(company.get('cnpj', '')),
                'name': company.get('razao_social', ''),
                'trade_name': company.get('nome_fantasia', ''),
                'status': company.get('descricao_situacao_cadastral', ''),
                'founding_date': company.get('data_inicio_atividade', ''),
                'legal_nature': company.get('natureza_juridica', ''),
                'size': company.get('porte', ''),
                'address': {},
                'activities': {}
            }

            # Address
            if 'estabelecimento' in company:
                est = company['estabelecimento']
                summary['address'] = {
                    'type': est.get('tipo_logradouro', ''),
                    'street': est.get('logradouro', ''),
                    'number': est.get('numero', ''),
                    'complement': est.get('complemento', ''),
                    'district': est.get('bairro', ''),
                    'city': est.get('cidade', {}).get('nome', ''),
                    'state': est.get('estado', {}).get('sigla', ''),
                    'zip_code': est.get('cep', ''),
                    'country': est.get('pais', {}).get('nome', '')
                }

            # Activities
            if 'estabelecimento' in company and 'atividades' in company['estabelecimento']:
                atv = company['estabelecimento']['atividades'][0]
                summary['activities'] = {
                    'primary': atv.get('descricao', ''),
                    'code': atv.get('codigo', 0)
                }

            return summary

        except Exception as e:
            return {
                'cnpj': self.format_cnpj(cnpj),
                'error': str(e)
            }