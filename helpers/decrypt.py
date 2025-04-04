import os
import random
import string

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from helpers.keyloaders import load_key_from_file

def decrypt_file(enc_path: str, key_file_path: str, output_path: str = None):
    with open(enc_path, "rb") as f:
        payload = f.read()

    # Extract nonce and extension
    nonce = payload[:12]
    name_len = payload[12]
    original_name = payload[13:13+name_len]
    encrypted_data = payload[13+name_len:]

    key = load_key_from_file(key_file_path)
    aesgcm = AESGCM(key)
    try:
        decrypted_data = aesgcm.decrypt(nonce, encrypted_data, associated_data=original_name)

        return {
            "decrypted_data": decrypted_data,
            "enc_path": enc_path,
            "original_name": original_name.decode()
        }
    except Exception as e:
        return None

def save_decrypted_to_file(decrypted, directory: str = None):
    enc_path = decrypted["enc_path"]
    original_name = decrypted["original_name"]
    if not directory:
        output_path = enc_path.replace(".enc", "") + f"_decrypted.{original_name}"
    else:
        output_path = os.path.join(directory, original_name)
    with open(output_path, "wb") as f:
        f.write(decrypted["decrypted_data"])
    return (f"Decrypted file saved to: {output_path}")
