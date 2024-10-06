import requests
import logging

import requests
import logging

# This script fetches the price of Monero (XMR) from various cryptocurrency exchanges.

class PriceFetcher:
    def __init__(self, http_client=None):
        self.http_client = http_client or requests.Session()
        self.binance_url = "https://api.binance.com/api/v3/ticker/price?symbol=XMRUSDT"
        self.kraken_url = "https://api.kraken.com/0/public/Ticker?pair=XMR{}"
        self.cryptocompare_url = "https://min-api.cryptocompare.com/data/price?fsym=XMR&tsyms={}"
        self.coingecko_url = "https://api.coingecko.com/api/v3/simple/price?ids=monero&vs_currencies={}"

    def fetch_from_coingecko(self, currency):
        """Fetch Monero price from CoinGecko."""
        url = self.coingecko_url.format(currency.lower())
        response = self.http_client.get(url)
        if response.status_code != 200:
            raise Exception(f"CoinGecko API error: {response.status_code}")
        data = response.json()
        price = data['monero'].get(currency.lower())
        if price is None:
            raise Exception("Currency not found in CoinGecko response")
        return price

    def fetch_from_binance(self):
        """Fetch Monero price from Binance (in USDT)."""
        response = self.http_client.get(self.binance_url)
        if response.status_code != 200:
            raise Exception(f"Binance API error: {response.status_code}")
        data = response.json()
        price_str = data.get('price')
        if price_str is None:
            raise Exception("Price not found in Binance response")
        return float(price_str)

    def fetch_from_kraken(self, currency):
        """Fetch Monero price from Kraken."""
        currency = currency.upper()
        url = self.kraken_url.format(currency)
        response = self.http_client.get(url)
        if response.status_code != 200:
            raise Exception(f"Kraken API error: {response.status_code}")
        data = response.json()
        if data.get('error'):
            raise Exception("Kraken API returned errors")
        
        pair = f"XXMRZ{currency}"
        result = data['result'].get(pair)
        if not result:
            raise Exception(f"Non-existent XMR pair on Kraken: {pair}")
        
        rate = result['c'][0]
        return float(rate)

    def fetch_from_cryptocompare(self, currency):
        """Fetch Monero price from CryptoCompare."""
        currency = currency.upper()
        url = self.cryptocompare_url.format(currency)
        response = self.http_client.get(url)
        if response.status_code != 200:
            raise Exception(f"CryptoCompare API error: {response.status_code}")
        data = response.json()
        price = data.get(currency)
        if price is None:
            raise Exception("Currency not found in CryptoCompare response")
        return price

    def fetch_xmr_price(self, currency):
        """Fetch Monero price from multiple sources with fallback."""
        sources = [
            (self.fetch_from_kraken, "kraken"),
            (self.fetch_from_coingecko, "coingecko"),
            (self.fetch_from_cryptocompare, "cryptocompare")
        ]

        for fetch_func, source_name in sources:
            try:
                price = fetch_func(currency)
                return price, source_name, None
            except Exception as e:
                logging.warning(f"Failed to fetch Monero price from {source_name}: {str(e)}")

        return 0, "", Exception("Failed to fetch Monero (XMR) price from all sources")

def main():
    logging.basicConfig(level=logging.INFO)
    client = PriceFetcher()
    currencies = ["USD", "EUR"]

    print("Fetching Monero (XMR) prices from various sources:")

    for currency in currencies:
        print(f"\nFetching Monero price in {currency}:")
        
        try:
            price = client.fetch_from_coingecko(currency)
            print(f"CoinGecko: 1 XMR = {price:.6f} {currency}")
        except Exception as e:
            logging.error(f"Failed to fetch Monero price in {currency} from CoinGecko: {str(e)}")

        try:
            price = client.fetch_from_cryptocompare(currency)
            print(f"CryptoCompare: 1 XMR = {price:.6f} {currency}")
        except Exception as e:
            logging.error(f"Failed to fetch Monero price in {currency} from CryptoCompare: {str(e)}")

        try:
            price = client.fetch_from_kraken(currency)
            print(f"Kraken: 1 XMR = {price:.6f} {currency}")
        except Exception as e:
            logging.error(f"Failed to fetch Monero price in {currency} from Kraken: {str(e)}")

    try:
        price = client.fetch_from_binance()
        print(f"\nBinance: 1 XMR = {price:.6f} USDT")
    except Exception as e:
        logging.error(f"Failed to fetch Monero price from Binance: {str(e)}")

    for currency in currencies:
        price, source, error = client.fetch_xmr_price(currency)
        if error:
            logging.error(f"Failed to get Monero rate in {currency} with fallbacks: {str(error)}")
        else:
            print(f"\nFallback method: 1 XMR = {price:.6f} {currency} (Source: {source})")

if __name__ == "__main__":
    main()
