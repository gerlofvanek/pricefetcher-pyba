#!/bin/bash

# This script fetches the price of Monero (XMR) from various cryptocurrency exchanges.

# Dependencies: curl, jq

# URLs for different exchanges
BINANCE_URL="https://api.binance.com/api/v3/ticker/price?symbol=XMRUSDT"
KRAKEN_URL="https://api.kraken.com/0/public/Ticker?pair=XMR"
CRYPTOCOMPARE_URL="https://min-api.cryptocompare.com/data/price?fsym=XMR&tsyms="
COINGECKO_URL="https://api.coingecko.com/api/v3/simple/price?ids=monero&vs_currencies="

# Function to fetch price from CoinGecko
fetch_from_coingecko() {
    local currency=$(echo $1 | tr '[:upper:]' '[:lower:]')
    local url="${COINGECKO_URL}${currency}"
    local response=$(curl -s "$url")
    echo $response | jq -r ".monero.$currency"
}

# Function to fetch price from Binance
fetch_from_binance() {
    local response=$(curl -s "$BINANCE_URL")
    echo $response | jq -r '.price'
}

# Function to fetch price from Kraken
fetch_from_kraken() {
    local currency=$(echo $1 | tr '[:lower:]' '[:upper:]')
    local url="${KRAKEN_URL}${currency}"
    local response=$(curl -s "$url")
    echo $response | jq -r ".result.XXMRZ${currency}.c[0]"
}

# Function to fetch price from CryptoCompare
fetch_from_cryptocompare() {
    local currency=$(echo $1 | tr '[:lower:]' '[:upper:]')
    local url="${CRYPTOCOMPARE_URL}${currency}"
    local response=$(curl -s "$url")
    echo $response | jq -r ".$currency"
}

# Function to fetch XMR price with fallback
fetch_xmr_price() {
    local currency=$1
    local price
    local source

    # Try Kraken
    price=$(fetch_from_kraken $currency 2>/dev/null)
    if [ $? -eq 0 ] && [ "$price" != "null" ]; then
        echo "$price kraken"
        return
    fi

    # Try CoinGecko
    price=$(fetch_from_coingecko $currency 2>/dev/null)
    if [ $? -eq 0 ] && [ "$price" != "null" ]; then
        echo "$price coingecko"
        return
    fi

    # Try CryptoCompare
    price=$(fetch_from_cryptocompare $currency 2>/dev/null)
    if [ $? -eq 0 ] && [ "$price" != "null" ]; then
        echo "$price cryptocompare"
        return
    fi

    echo "0 error"
}

# Main function
main() {
    local currencies=("USD" "EUR")

    echo "Fetching Monero (XMR) prices from various sources:"

    for currency in "${currencies[@]}"; do
        echo -e "\nFetching Monero price in $currency:"

        price=$(fetch_from_coingecko $currency)
        [ "$price" != "null" ] && echo "CoinGecko: 1 XMR = $price $currency" || echo "Failed to fetch from CoinGecko"

        price=$(fetch_from_cryptocompare $currency)
        [ "$price" != "null" ] && echo "CryptoCompare: 1 XMR = $price $currency" || echo "Failed to fetch from CryptoCompare"

        price=$(fetch_from_kraken $currency)
        [ "$price" != "null" ] && echo "Kraken: 1 XMR = $price $currency" || echo "Failed to fetch from Kraken"
    done

    price=$(fetch_from_binance)
    [ "$price" != "null" ] && echo -e "\nBinance: 1 XMR = $price USDT" || echo "Failed to fetch from Binance"

    for currency in "${currencies[@]}"; do
        read price source <<< $(fetch_xmr_price $currency)
        if [ "$source" != "error" ]; then
            echo -e "\nFallback method: 1 XMR = $price $currency (Source: $source)"
        else
            echo "Failed to get Monero rate in $currency with fallbacks"
        fi
    done
}

# Run the main function
main
