import requests

def get_currency_input(currencies):
    """
    Function to handle user input for currency codes and amount, ensuring valid currency codes.
    Returns a tuple (initial_currency, target_currency, amount).
    """
    print("Available currencies:")
    for currency in currencies:
        print(currency, end=" ")

    print()  # Adding a newline after the currency codes list
    
    while True:
        init_currency = input("Enter the initial currency code: ").upper()
        target_currency = input("Enter the target currency code: ").upper()

        if init_currency not in currencies or target_currency not in currencies:
            print("Invalid currency code entered. Please use a valid currency code.")
            continue

        try:
            amount = float(input("Enter an amount: "))
            if amount == 0:
                raise ValueError("Amount cannot be zero.")
            return init_currency, target_currency, amount
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid number greater than zero.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

def fetch_supported_currencies():
    """
    Fetch the list of supported currencies from the API.
    Returns a list of currency codes.
    """
    url = "https://api.apilayer.com/fixer/symbols"
    headers = {
        "apikey": "VvVzYCurdo2MzlZIVR1LZYXQeb8IWRmZ"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        
        result = response.json()
        if 'symbols' not in result:
            raise ValueError("Error retrieving symbols.")
        
        return list(result['symbols'].keys())  # Return a list of currency codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        return []

def fetch_conversion_rate(init_currency, target_currency, amount):
    """
    Fetch the conversion rate from the API and return the result.
    Returns a tuple (success, converted_amount, error_message).
    """
    url = f"https://api.apilayer.com/fixer/convert?to={target_currency}&from={init_currency}&amount={amount}"
    headers = {
        "apikey": "VvVzYCurdo2MzlZIVR1LZYXQeb8IWRmZ"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        
        result = response.json()
        converted_amount = result.get('result')

        if converted_amount is None:
            return False, None, "Invalid currency codes or API issue."
        
        return True, converted_amount, None
    except requests.exceptions.RequestException as e:
        return False, None, f"Error fetching data from the API: {e}"

def main():
    """
    Main function to drive the currency conversion process.
    """
    currencies = fetch_supported_currencies()
    if not currencies:
        print("Failed to retrieve available currencies. Exiting.")
        return

    init_currency, target_currency, amount = get_currency_input(currencies)

    success, converted_amount, error_message = fetch_conversion_rate(init_currency, target_currency, amount)

    if success:
        print(f"{amount} {init_currency} = {converted_amount} {target_currency}")
    else:
        print(f"Conversion failed: {error_message}")

if __name__ == "__main__":
    main()
