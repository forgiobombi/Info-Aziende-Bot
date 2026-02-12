"""
OpenAPI.it API Client for fetching Italian company information
"""
import aiohttp
import json
from datetime import datetime
from typing import Optional, Dict, Any


class OpenAPIClient:
    """Client for interacting with OpenAPI.it Company Advanced Italia API"""
    
    BASE_URL = "https://openapi.it/api/impresa"
    
    def __init__(self, api_token: str):
        """
        Initialize the API client
        
        Args:
            api_token: OpenAPI.it API token
        """
        self.api_token = api_token
        self.api_calls_count = 0
        self.last_reset = datetime.now()
        
    async def get_company_info(self, partita_iva: str) -> Dict[str, Any]:
        """
        Fetch company information by Partita IVA (VAT number)
        
        Args:
            partita_iva: Italian VAT number (Partita IVA)
            
        Returns:
            Dictionary containing company information
            
        Raises:
            aiohttp.ClientError: If API request fails
        """
        # Validate Partita IVA format (11 digits)
        if not partita_iva.isdigit() or len(partita_iva) != 11:
            raise ValueError("Partita IVA must be 11 digits")
        
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/json"
        }
        
        # The endpoint format for OpenAPI.it is typically /api/impresa/{piva}
        url = f"{self.BASE_URL}/{partita_iva}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                self.api_calls_count += 1
                
                if response.status == 200:
                    data = await response.json()
                    return data
                elif response.status == 404:
                    return {"error": "Company not found", "status": 404}
                elif response.status == 401:
                    return {"error": "Invalid API token", "status": 401}
                elif response.status == 429:
                    return {"error": "API rate limit exceeded", "status": 429}
                else:
                    error_text = await response.text()
                    return {
                        "error": f"API error: {response.status}",
                        "status": response.status,
                        "details": error_text
                    }
    
    def get_api_usage(self) -> Dict[str, Any]:
        """
        Get current API usage statistics
        
        Returns:
            Dictionary with API usage information
        """
        time_since_reset = datetime.now() - self.last_reset
        return {
            "calls_count": self.api_calls_count,
            "last_reset": self.last_reset.isoformat(),
            "hours_since_reset": time_since_reset.total_seconds() / 3600,
            "note": "Free tier typically allows 100-500 requests per day"
        }
    
    def reset_usage_counter(self):
        """Reset the API usage counter"""
        self.api_calls_count = 0
        self.last_reset = datetime.now()
