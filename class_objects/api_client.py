

import requests
import json
from typing import Dict, Any

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Dict[str, Any] = None, headers: Dict[str, str] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def soap_request(self, endpoint: str, soap_action: str, xml: str, headers: Dict[str, str] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        headers = headers or {}
        headers.update({
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': soap_action
        })
        response = requests.post(url, data=xml, headers=headers)
        response.raise_for_status()
        return response.content  # You might need to parse the XML response

    def custom_request(self, method: str, endpoint: str, data: Any = None, headers: Dict[str, str] = None) -> Any:
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()