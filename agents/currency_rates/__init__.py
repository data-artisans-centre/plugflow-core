import json
from itertools import islice
from core.base import AgentBase
from log import logger
import requests

class CurrencyRatesAgent(AgentBase):
    """Agent to fetch Currency exchange rates."""
    valid_currency_codes = [
    "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", 
    "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL", 
    "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF", "CLP", "CNY", 
    "COP", "CRC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", 
    "ERN", "ETB", "EUR", "FJD", "FKP", "FOK", "GBP", "GEL", "GGP", "GHS", 
    "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", 
    "IDR", "ILS", "IMP", "INR", "IQD", "IRR", "ISK", "JEP", "JMD", "JOD", 
    "JPY", "KES", "KGS", "KHR", "KID", "KMF", "KRW", "KWD", "KYD", "KZT", 
    "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", 
    "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MYR", "MZN", 
    "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", 
    "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", 
    "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SOS", "SRD", "SSP", 
    "STN", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", 
    "TVD", "TWD", "TZS", "UAH", "UGX", "USD", "UYU", "UZS", "VES", "VND", 
    "VUV", "WST", "XAF", "XCD", "XDR", "XOF", "XPF", "YER", "ZAR", "ZMW", 
    "ZWL"
    ]

    def execute(self, api_key, base_currency, target_currency):
        """
        Fetch the conversion rate for two currencies.

        Args:
            api_key (str): The API key used to authenticate and access the API.
            base_currency (str): The ISO 4217 three-letter currency code representing the currency to convert from.  
            target_currency (str): The ISO 4217 three-letter currency code representing the currency to convert to.

        Returns:
            str: JSON-formatted string containing fetched currency rates.

        Raises:
            ValueError: If the base_currency code or target_currency code is not valid

        """

        if (base_currency not in self.valid_currency_codes) or (target_currency not in self.valid_currency_codes):
            raise ValueError(f"Invalid currency code. Valid currency codes are :{', '.join(self.valid_currency_codes)}")
        
        try:
            logger.info(f"Fetching currency conversion rate from {base_currency} to {target_currency}")
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}"
            response = requests.get(url)
            response.raise_for_status()
            
            rate = response.json()
            rate_readable = json.dumps(rate, indent = 4)
            #Log the JSON-formatted rate
            print(rate_readable)
            return rate_readable
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise ValueError("Failed to fetch currency rates. ") from e


    def health_check(self, api_key):
        """
        Check if the currency rate API is functional.

        Args:
            api_key (str): API key for the currency rate service.

        Returns:
            dict: Health status of the plugin.
        """
        if not api_key or not isinstance(api_key, str):
            logger.error("Invalid API key provided for health check.")
            return {"status": "unhealthy", "message": "Invalid API key."}

        try:
            logger.info("Performing health check for the currency rate API...")

            base_currency = "USD"
            target_currency = "GBP"
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}"

           
            response = requests.get(url, timeout=5)
            response.raise_for_status()  

            # Check the response content
            data = response.json()
            if data.get("result") != "success":
                logger.error(f"Health check failed: Unexpected response content - {data}")
                return {"status": "unhealthy", "message": "Unexpected response from API."}

            logger.info("Health check passed. API is functional.")
            return {"status": "healthy", "message": "Service is available."}

        except requests.exceptions.Timeout:
            logger.error("Health check failed: API request timed out.")
            return {"status": "unhealthy", "message": "API request timed out."}

        except requests.exceptions.RequestException as e:
            logger.error(f"Health check failed: HTTP error - {e}")
            return {"status": "unhealthy", "message": f"HTTP error: {str(e)}"}

        except Exception as e:
            logger.error(f"Health check failed: Unexpected error - {e}")
            return {"status": "unhealthy", "message": f"Unexpected error: {str(e)}"}
