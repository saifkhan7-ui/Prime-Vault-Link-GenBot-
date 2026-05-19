import base64

def encode_id(message_id: int) -> str:
    string_id = f"file-{message_id}"
    return base64.urlsafe_b64encode(string_id.encode("ascii")).decode("ascii").rstrip("=")

def decode_id(base64_string: str) -> int:
    try:
        base64_string += "=" * ((4 - len(base64_string) % 4) % 4)
        decoded_str = base64.urlsafe_b64decode(base64_string.encode("ascii")).decode("ascii")
        if decoded_str.startswith("file-"):
            return int(decoded_str.split("-")[1])
        return 0
    except:
        return 0
