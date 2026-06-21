"""QR code generator for crypto addresses."""
import qrcode, io, base64

def generate_qr(data: str) -> str:
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def generate_crypto_qr(address: str, network: str, amount: float = None) -> str:
    uri = build_deep_link(network, address, amount)
    return generate_qr(uri)

def build_deep_link(network: str, address: str, amount: float = None) -> str:
    schemes = {"btc":"bitcoin","eth":"ethereum","usdc_erc20":"ethereum","usdt_trc20":"tron"}
    scheme = schemes.get(network, "ethereum")
    link = f"{scheme}:{address}"
    if amount: link += f"?amount={amount}"
    return link
