import os
import binascii

def generate_random_bytes(length):
    """Generate cryptographically secure random bytes"""
    return os.urandom(length)

def generate_hmac_key():
    """Generate 32-byte HMAC key (for SHA-256)"""
    return generate_random_bytes(32)

def generate_aes_key():
    """Generate 16-byte AES key"""
    return generate_random_bytes(16)

def generate_fixed_iv():
    """Generate 16-byte IV (for task2)"""
    return generate_random_bytes(16)

if __name__ == "__main__":
    secrets = {
        'TASK1_KEY': generate_aes_key(),
        'TASK1_HMAC': generate_hmac_key(),
        'TASK2_KEY1': generate_aes_key(),
        'TASK2_IV1': generate_fixed_iv(),
        'TASK2_KEY2': generate_aes_key(),
        'TASK2_IV2': generate_fixed_iv(),
    }
    
    for k, v in secrets.items():
        print(f"{k}: \"{binascii.hexlify(v).decode('utf-8')}\"")
