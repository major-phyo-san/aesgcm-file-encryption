from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_key() -> bytes:
    return AESGCM.generate_key(bit_length=256)  # 32 bytes