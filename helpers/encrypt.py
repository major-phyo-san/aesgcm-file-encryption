import os
import random
import string

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from helpers.keyloaders import load_key_from_file

def encrypt_file(file_path: str, key_file_path: str, output_path: str = None):
    try:
        key = load_key_from_file(key_file_path)
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)  # AES-GCM standard
    except Exception as e:
        raise Exception("Key loading failed")
    
    # Load original file content
    with open(file_path, "rb") as f:
        data = f.read()

    # Extract file extension
    ext = os.path.splitext(file_path)[1][1:]  # exclude dot
    ext_bytes = ext.encode()
    if len(ext_bytes) > 255:
        raise ValueError("File extension too long")

    # Metadata to protect
    file_name = os.path.basename(file_path).encode()
    associated_data = file_name  # Can be extended to JSON etc.

    # Encrypt with the format [12-byte nonce][.ext length (1 byte)][extension][ciphertext][auth_tag]
    encrypted_data = aesgcm.encrypt(nonce, data, associated_data=associated_data)

    # Store: nonce + filename length + filename + ciphertext
    payload = (
        nonce
        + bytes([len(file_name)])
        + file_name
        + encrypted_data
    )

    # Prepare final format
    # payload = nonce + bytes([len(ext_bytes)]) + ext_bytes + encrypted_data

    return payload

def save_encrypted_to_file(encrypted, directory):
    encrypted_file_path = os.path.join(directory, generate_random_string() + ".enc")
    # output_path = file_path + ".enc"
    try:
        with open(encrypted_file_path, "wb") as f:
            f.write(encrypted)
    except Exception as e:
        return None
    return (f"Encrypted file saved to: {encrypted_file_path}")

def generate_random_string(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))