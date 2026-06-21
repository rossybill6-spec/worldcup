"""Deep link generator for crypto wallet apps."""
def generate_deep_link(network: str, address: str, amount: float = None) -> str:
    from app.utils.qr_code import build_deep_link
    return build_deep_link(network, address, amount)

def get_wallet_deep_link(network: str, address: str, amount: float) -> dict:
    link = generate_deep_link(network, address, amount)
    return {"deep_link": link, "network": network, "address": address, "amount": amount}
