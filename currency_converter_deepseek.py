import requests
from typing import Tuple, List, Optional, Dict

class CurrencyConverter:
    """
    A professional currency converter using the Fixer API.
    Handles currency code validation, API communication, and conversion calculations.
    """
    
    API_BASE_URL = "https://api.apilayer.com/fixer"
    HEADERS = {
        "apikey": "VvVzYCurdo2MzlZIVR1LZYXQeb8IWRmZ"
    }
    
    # Comprehensive currency names dictionary
    CURRENCY_NAMES = {
        "AED": "United Arab Emirates Dirham",
        "AFN": "Afghan Afghani",
        "ALL": "Albanian Lek",
        "AMD": "Armenian Dram",
        "ANG": "Netherlands Antillean Guilder",
        "AOA": "Angolan Kwanza",
        "ARS": "Argentine Peso",
        "AUD": "Australian Dollar",
        "AWG": "Aruban Florin",
        "AZN": "Azerbaijani Manat",
        "BAM": "Bosnia-Herzegovina Convertible Mark",
        "BBD": "Barbadian Dollar",
        "BDT": "Bangladeshi Taka",
        "BGN": "Bulgarian Lev",
        "BHD": "Bahraini Dinar",
        "BIF": "Burundian Franc",
        "BMD": "Bermudian Dollar",
        "BND": "Brunei Dollar",
        "BOB": "Bolivian Boliviano",
        "BRL": "Brazilian Real",
        "BSD": "Bahamian Dollar",
        "BTC": "Bitcoin",
        "BTN": "Bhutanese Ngultrum",
        "BWP": "Botswanan Pula",
        "BYN": "Belarusian Ruble",
        "BYR": "Belarusian Ruble (pre-2016)",
        "BZD": "Belize Dollar",
        "CAD": "Canadian Dollar",
        "CDF": "Congolese Franc",
        "CHF": "Swiss Franc",
        "CLF": "Chilean Unit of Account (UF)",
        "CLP": "Chilean Peso",
        "CNH": "Chinese Yuan (Offshore)",
        "CNY": "Chinese Yuan",
        "COP": "Colombian Peso",
        "CRC": "Costa Rican Colón",
        "CUC": "Cuban Convertible Peso",
        "CUP": "Cuban Peso",
        "CVE": "Cape Verdean Escudo",
        "CZK": "Czech Republic Koruna",
        "DJF": "Djiboutian Franc",
        "DKK": "Danish Krone",
        "DOP": "Dominican Peso",
        "DZD": "Algerian Dinar",
        "EGP": "Egyptian Pound",
        "ERN": "Eritrean Nakfa",
        "ETB": "Ethiopian Birr",
        "EUR": "Euro",
        "FJD": "Fijian Dollar",
        "FKP": "Falkland Islands Pound",
        "GBP": "British Pound Sterling",
        "GEL": "Georgian Lari",
        "GGP": "Guernsey Pound",
        "GHS": "Ghanaian Cedi",
        "GIP": "Gibraltar Pound",
        "GMD": "Gambian Dalasi",
        "GNF": "Guinean Franc",
        "GTQ": "Guatemalan Quetzal",
        "GYD": "Guyanaese Dollar",
        "HKD": "Hong Kong Dollar",
        "HNL": "Honduran Lempira",
        "HRK": "Croatian Kuna",
        "HTG": "Haitian Gourde",
        "HUF": "Hungarian Forint",
        "IDR": "Indonesian Rupiah",
        "ILS": "Israeli New Sheqel",
        "IMP": "Manx pound",
        "INR": "Indian Rupee",
        "IQD": "Iraqi Dinar",
        "IRR": "Iranian Rial",
        "ISK": "Icelandic Króna",
        "JEP": "Jersey Pound",
        "JMD": "Jamaican Dollar",
        "JOD": "Jordanian Dinar",
        "JPY": "Japanese Yen",
        "KES": "Kenyan Shilling",
        "KGS": "Kyrgystani Som",
        "KHR": "Cambodian Riel",
        "KMF": "Comorian Franc",
        "KPW": "North Korean Won",
        "KRW": "South Korean Won",
        "KWD": "Kuwaiti Dinar",
        "KYD": "Cayman Islands Dollar",
        "KZT": "Kazakhstani Tenge",
        "LAK": "Laotian Kip",
        "LBP": "Lebanese Pound",
        "LKR": "Sri Lankan Rupee",
        "LRD": "Liberian Dollar",
        "LSL": "Lesotho Loti",
        "LTL": "Lithuanian Litas",
        "LVL": "Latvian Lats",
        "LYD": "Libyan Dinar",
        "MAD": "Moroccan Dirham",
        "MDL": "Moldovan Leu",
        "MGA": "Malagasy Ariary",
        "MKD": "Macedonian Denar",
        "MMK": "Myanma Kyat",
        "MNT": "Mongolian Tugrik",
        "MOP": "Macanese Pataca",
        "MRU": "Mauritanian Ouguiya",
        "MUR": "Mauritian Rupee",
        "MVR": "Maldivian Rufiyaa",
        "MWK": "Malawian Kwacha",
        "MXN": "Mexican Peso",
        "MYR": "Malaysian Ringgit",
        "MZN": "Mozambican Metical",
        "NAD": "Namibian Dollar",
        "NGN": "Nigerian Naira",
        "NIO": "Nicaraguan Córdoba",
        "NOK": "Norwegian Krone",
        "NPR": "Nepalese Rupee",
        "NZD": "New Zealand Dollar",
        "OMR": "Omani Rial",
        "PAB": "Panamanian Balboa",
        "PEN": "Peruvian Nuevo Sol",
        "PGK": "Papua New Guinean Kina",
        "PHP": "Philippine Peso",
        "PKR": "Pakistani Rupee",
        "PLN": "Polish Zloty",
        "PYG": "Paraguayan Guarani",
        "QAR": "Qatari Rial",
        "RON": "Romanian Leu",
        "RSD": "Serbian Dinar",
        "RUB": "Russian Ruble",
        "RWF": "Rwandan Franc",
        "SAR": "Saudi Riyal",
        "SBD": "Solomon Islands Dollar",
        "SCR": "Seychellois Rupee",
        "SDG": "Sudanese Pound",
        "SEK": "Swedish Krona",
        "SGD": "Singapore Dollar",
        "SHP": "Saint Helena Pound",
        "SLE": "Sierra Leonean Leone",
        "SLL": "Sierra Leonean Leone (old)",
        "SOS": "Somali Shilling",
        "SRD": "Surinamese Dollar",
        "STD": "São Tomé and Príncipe Dobra",
        "SVC": "Salvadoran Colón",
        "SYP": "Syrian Pound",
        "SZL": "Swazi Lilangeni",
        "THB": "Thai Baht",
        "TJS": "Tajikistani Somoni",
        "TMT": "Turkmenistani Manat",
        "TND": "Tunisian Dinar",
        "TOP": "Tongan Paʻanga",
        "TRY": "Turkish Lira",
        "TTD": "Trinidad and Tobago Dollar",
        "TWD": "New Taiwan Dollar",
        "TZS": "Tanzanian Shilling",
        "UAH": "Ukrainian Hryvnia",
        "UGX": "Ugandan Shilling",
        "USD": "United States Dollar",
        "UYU": "Uruguayan Peso",
        "UZS": "Uzbekistan Som",
        "VEF": "Venezuelan Bolívar Fuerte",
        "VES": "Venezuelan Bolívar Soberano",
        "VND": "Vietnamese Dong",
        "VUV": "Vanuatu Vatu",
        "WST": "Samoan Tala",
        "XAF": "CFA Franc BEAC",
        "XAG": "Silver Ounce",
        "XAU": "Gold Ounce",
        "XCD": "East Caribbean Dollar",
        "XDR": "Special Drawing Rights",
        "XOF": "CFA Franc BCEAO",
        "XPF": "CFP Franc",
        "YER": "Yemeni Rial",
        "ZAR": "South African Rand",
        "ZMK": "Zambian Kwacha (pre-2013)",
        "ZMW": "Zambian Kwacha",
        "ZWL": "Zimbabwean Dollar"
    }
    
    def __init__(self):
        self.supported_currencies = self._fetch_supported_currencies()
    
    def _fetch_supported_currencies(self) -> List[str]:
        """
        Fetch the list of supported currencies from the API.
        
        Returns:
            List[str]: A list of supported currency codes
            
        Raises:
            RuntimeError: If unable to fetch currencies from API
        """
        endpoint = f"{self.API_BASE_URL}/symbols"
        
        try:
            response = requests.get(endpoint, headers=self.HEADERS)
            response.raise_for_status()
            
            data = response.json()
            if not data.get('success', False) or 'symbols' not in data:
                raise ValueError("Invalid API response structure")
                
            return list(data['symbols'].keys())
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")
        except (ValueError, KeyError) as e:
            raise RuntimeError(f"Failed to parse API response: {str(e)}")
    
    def _validate_currency_code(self, code: str) -> bool:
        """
        Validate if a currency code is supported.
        
        Args:
            code (str): Currency code to validate
            
        Returns:
            bool: True if code is valid/supported
        """
        return code in self.supported_currencies
    
    def _display_available_currencies(self) -> None:
        """Display available currencies in a user-friendly format."""
        print("\nAvailable Currencies:")
        print("=" * 40)
        print("{:<8} {:<35}".format("Code", "Currency Name"))
        print("-" * 40)
        
        # Sort currencies alphabetically by code
        sorted_currencies = sorted(self.supported_currencies)
        
        # Display in columns (5 per row)
        for i in range(0, len(sorted_currencies), 5):
            row = sorted_currencies[i:i+5]
            print("  ".join([f"{code:<8}" for code in row]))
        
        print("\nFor full currency names, please refer to the documentation.\n")
    
    def _get_user_input(self) -> Tuple[str, str, float]:
        """
        Get and validate user input for currency conversion.
        
        Returns:
            Tuple[str, str, float]: (from_currency, to_currency, amount)
            
        Raises:
            ValueError: If input validation fails
        """
        self._display_available_currencies()
        
        while True:
            try:
                from_curr = input("\nEnter source currency code: ").strip().upper()
                if not self._validate_currency_code(from_curr):
                    raise ValueError(f"Unsupported source currency: {from_curr}")
                
                to_curr = input("Enter target currency code: ").strip().upper()
                if not self._validate_currency_code(to_curr):
                    raise ValueError(f"Unsupported target currency: {to_curr}")
                if from_curr == to_curr:
                    raise ValueError("Source and target currencies cannot be the same")
                
                amount_str = input("Enter amount to convert: ").strip()
                if not amount_str.replace('.', '', 1).isdigit():
                    raise ValueError("Amount must be a positive number")
                
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                
                # Display the currency names for confirmation
                print(f"\nConverting {amount:.2f} {from_curr} ({self.CURRENCY_NAMES.get(from_curr, 'Unknown currency')}) "
                      f"to {to_curr} ({self.CURRENCY_NAMES.get(to_curr, 'Unknown currency')})")
                
                return from_curr, to_curr, amount
                
            except ValueError as e:
                print(f"\nError: {str(e)}. Please try again.")
    
    def convert_currency(self, from_curr: str, to_curr: str, amount: float) -> Tuple[bool, Optional[float], Optional[str]]:
        """
        Convert between currencies using the Fixer API.
        
        Args:
            from_curr (str): Source currency code
            to_curr (str): Target currency code
            amount (float): Amount to convert
            
        Returns:
            Tuple[bool, Optional[float], Optional[str]]: 
                (success, converted_amount, error_message)
        """
        endpoint = f"{self.API_BASE_URL}/convert"
        params = {
            "from": from_curr,
            "to": to_curr,
            "amount": amount
        }
        
        try:
            response = requests.get(endpoint, headers=self.HEADERS, params=params)
            response.raise_for_status()
            
            data = response.json()
            if not data.get('success', False):
                return False, None, data.get('error', {}).get('info', "Conversion failed")
                
            return True, data['result'], None
            
        except requests.exceptions.RequestException as e:
            return False, None, f"API request failed: {str(e)}"
        except (KeyError, ValueError) as e:
            return False, None, f"Failed to parse API response: {str(e)}"
    
    def run(self) -> None:
        """
        Run the currency converter application.
        """
        print("\n=== Currency Converter ===")
        print("=" * 25)
        
        if not self.supported_currencies:
            print("Error: Failed to initialize supported currencies. Please try again later.")
            return
        
        try:
            from_curr, to_curr, amount = self._get_user_input()
            success, result, error = self.convert_currency(from_curr, to_curr, amount)
            
            if success:
                print(f"\nConversion Result:")
                print("=" * 40)
                print(f"{amount:.2f} {from_curr} ({self.CURRENCY_NAMES.get(from_curr, 'Unknown currency')})")
                print(f"= {result:.2f} {to_curr} ({self.CURRENCY_NAMES.get(to_curr, 'Unknown currency')})")
                print("=" * 40)
            else:
                print(f"\nError: {error}")
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {str(e)}")

def main():
    """Entry point for the currency converter application."""
    try:
        converter = CurrencyConverter()
        converter.run()
    except Exception as e:
        print(f"Failed to initialize currency converter: {str(e)}")

if __name__ == "__main__":
    main()