# PriceFetcher (Python & Bash Version)

This repository contains a **Python** and **Bash** implementation of **PriceFetcher**, originally written in Go by [sausagenoods](https://github.com/sausagenoods). You can find the Go version of PriceFetcher [here](https://github.com/monero-atm/pricefetcher).

## Project Overview

This tool fetches real-time prices for Monero (XMR) from various cryptocurrency exchanges using both Python and Bash. It supports multiple exchanges like Binance, Kraken, CoinGecko, and CryptoCompare, and fetches prices in multiple currencies (e.g., USD, EUR). The Python and Bash versions offer flexibility depending on your environment or preferences.

## Features

- Fetches Monero (XMR) prices from multiple exchanges (Binance, Kraken, CoinGecko, and CryptoCompare).
- Supports fetching prices in various currencies (USD, EUR, etc.).
- Includes a fallback mechanism if one exchange fails.
- Lightweight, with minimal dependencies.
- Written in both Python and Bash to accommodate different environments.

## Installation and Usage

### Python Version

#### Prerequisites

- Python 3.x
- `requests` and `logging` Python libraries (install using `pip`)

#### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/gerlofvanek/pricefetcher-pyba.git
    ```

2. Navigate to the project directory:
    ```bash
    cd pricefetcher-pyba
    ```

3. Install Python dependencies:
    ```bash
    pip install requests logging
    ```

4. Run the Python script:
    ```bash
    python pricefetcher.py
    ```

### Bash Version

#### Prerequisites

- Bash (available on most Unix-like systems)
- `curl` and `jq` (install using your package manager, e.g., `sudo apt install curl jq` on Ubuntu)

#### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/gerlofvanek/pricefetcher-pyba.git
    ```

2. Navigate to the project directory:
    ```bash
    cd pricefetcher-pyba
    ```

3. Make the script executable (if needed):
    ```bash
    chmod +x pricefetcher.sh
    ```

4. Run the Bash script:
    ```bash
    ./pricefetcher.sh
    ```

## How It Works

### Python Version

The Python script `pricefetcher.py` fetches Monero prices from different exchanges using the following functions:
- **CoinGecko**: `fetch_from_coingecko`
- **Binance**: `fetch_from_binance`
- **Kraken**: `fetch_from_kraken`
- **CryptoCompare**: `fetch_from_cryptocompare`

It supports fetching prices for multiple currencies (USD, EUR), and includes a fallback mechanism to try different exchanges if one fails. The script logs errors and outputs prices to the console.

### Bash Version

The Bash script `pricefetcher.sh` fetches Monero prices using `curl` and processes the results with `jq`:
- Fetches from **CoinGecko**, **Binance**, **Kraken**, and **CryptoCompare**.
- Includes fallback logic to try different exchanges if one fails.
- Supports multiple currencies (USD, EUR).

## Example Output

Here’s what the output might look like:

### Python Version:

Fetching Monero (XMR) prices from various sources:

Fetching Monero price in USD: CoinGecko: 1 XMR = 154.670000 USD CryptoCompare: 1 XMR = 154.670000 USD Kraken: 1 XMR = 154.650000 USD

Binance: 1 XMR = 154.800000 USDT

Fallback method: 1 XMR = 154.670000 USD (Source: coingecko)


### Bash Version:

Fetching Monero (XMR) prices from various sources:

Fetching Monero price in USD: CoinGecko: 1 XMR = 154.670000 USD CryptoCompare: 1 XMR = 154.670000 USD Kraken: 1 XMR = 154.650000 USD

Binance: 1 XMR = 154.800000 USDT

Fallback method: 1 XMR = 154.670000 USD (Source: coingecko)


## Configuration

In both versions, you can modify the supported exchanges and currencies. The default configuration includes USD and EUR. To add more currencies, update the `currencies` list in the Python script (`pricefetcher.py`) or modify the array in the Bash script (`pricefetcher.sh`).

## Contributing

Feel free to contribute to this project by submitting pull requests or issues. Whether it's bug fixes, new features, or more exchange integrations, contributions are welcome.

## Donations

If you find this project helpful, a little tip can go a long way in supporting future development! You can donate Monero (XMR) to the following address:

**Monero XMR Address**: `85pg5VsuthbJqiTSuihyBASuvYUXBViW7CX4fLKaPNRmM2Z1tFSa1PpF8PpM6QXQUpVDHjXi3xVae86UDtqEZGeCByChSM7`

Thank you for your support!

## Credits

- Original Go version of PriceFetcher by [sausagenoods](https://github.com/sausagenoods) - [Go PriceFetcher](https://github.com/monero-atm/pricefetcher).
- Python and Bash version created by [gerlofvanek](https://github.com/gerlofvanek).
