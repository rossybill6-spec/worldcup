"""Deposit method constants."""
DEPOSIT_METHODS = [
    {"name": "Crypto", "slug": "crypto", "icon": "bitcoin", "description": "Deposit using Bitcoin, Ethereum, USDC, or USDT"},
    {"name": "ACH Transfer", "slug": "ach", "icon": "bank", "description": "Transfer from your bank account via ACH"},
    {"name": "Wire Transfer", "slug": "wire", "icon": "wire", "description": "Send a domestic or international wire"},
    {"name": "Mobile Check Deposit", "slug": "check", "icon": "check", "description": "Deposit a check using your phone camera"},
    {"name": "Cash Deposit", "slug": "cash", "icon": "cash", "description": "Deposit cash at a partner location"},
    {"name": "Direct Deposit", "slug": "direct_deposit", "icon": "direct", "description": "Set up direct deposit with your employer"},
    {"name": "P2P Transfer", "slug": "p2p", "icon": "people", "description": "Receive from another BankApp user"},
]
