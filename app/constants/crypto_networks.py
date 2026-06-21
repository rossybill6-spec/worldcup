"""Default crypto network configurations."""
CRYPTO_NETWORKS = [
    {
        "name": "Bitcoin", "symbol": "BTC", "slug": "btc", "network_type": "bitcoin",
        "admin_wallet_address": "bc1qadminbitcoinaddressplaceholder",
        "min_confirmations": "3", "deep_link_scheme": "bitcoin",
        "block_explorer_url": "https://www.blockchain.com/explorer/transactions/btc",
    },
    {
        "name": "Ethereum", "symbol": "ETH", "slug": "eth", "network_type": "ethereum",
        "admin_wallet_address": "0x742d35Cc6634C0539085a3c1E39c7f5eC5D8d9a1",
        "min_confirmations": "12", "deep_link_scheme": "ethereum",
        "block_explorer_url": "https://etherscan.io/tx",
    },
    {
        "name": "USD Coin", "symbol": "USDC", "slug": "usdc_erc20", "network_type": "erc20",
        "contract_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "admin_wallet_address": "0x742d35Cc6634C0539085a3c1E39c7f5eC5D8d9a1",
        "min_confirmations": "12", "deep_link_scheme": "ethereum",
        "block_explorer_url": "https://etherscan.io/tx",
    },
    {
        "name": "Tether USD", "symbol": "USDT", "slug": "usdt_trc20", "network_type": "trc20",
        "contract_address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
        "admin_wallet_address": "TAdminTRONaddressplaceholder123",
        "min_confirmations": "19", "deep_link_scheme": "tron",
        "block_explorer_url": "https://tronscan.org/#/transaction",
    },
]
