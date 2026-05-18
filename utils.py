import base64

# 🔒 Encode: Message ID ko secret text banayega
async def encode_id(message_id: int) -> str:
    # Hum apna 'pv-' (Prime Vault) stamp laga rahe hain!
    string_id = f"pv-{message_id}"
    string_bytes = string_id.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    return base64_bytes.decode("ascii").rstrip("=")

# 🔓 Decode: Secret text ko wapas Message ID banayega
async def decode_id(base64_string: str) -> int:
    try:
        # Base64 padding fix
        base64_string += "=" * ((4 - len(base64_string) % 4) % 4)
        string_bytes = base64.urlsafe_b64decode(base64_string.encode("ascii"))
        decoded_str = string_bytes.decode("ascii")
        
        # Apna 'pv-' stamp check karke asli ID nikalna
        if decoded_str.startswith("pv-"):
            return int(decoded_str.split("-")[1])
        return 0
    except Exception:
        return 0
      
