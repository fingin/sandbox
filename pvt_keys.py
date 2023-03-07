import hashlib
import binascii

def generate_eth_key():
    # Generate a random 256-bit private key
    private_key = hashlib.sha256(str.encode("my secret seed")).hexdigest()
    
    # Convert the private key from hex to bytes
    private_key_bytes = bytes.fromhex(private_key)
    
    # Derive the public key from the private key
    public_key_bytes = hashlib.sha3_256(private_key_bytes).digest()
    
    # Take the last 20 bytes of the public key as the Ethereum address
    ethereum_address = public_key_bytes[-20:]
    
    # Convert the Ethereum address to a human-readable format
    ethereum_address_str = '0x' + binascii.hexlify(ethereum_address).decode('utf-8')
    
    return (private_key, ethereum_address_str)

private_key, public_address = generate_eth_key()

print("Private key:", private_key)
print("Public address:", public_address)

# Define the secp256k1 curve parameters
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

def get_public_key(priv_key):
    # Convert the private key from hex to an integer
    d = int(priv_key, 16)
    
    # Calculate the public key using the secp256k1 curve
    Qx, Qy = multiply(Gx, Gy, d)
    
    # Convert the public key coordinates to bytes
    Qx_bytes = Qx.to_bytes(32, byteorder='big')
    Qy_bytes = Qy.to_bytes(32, byteorder='big')
    
    # Concatenate the public key coordinates to form the uncompressed public key
    public_key_bytes = b'\x04' + Qx_bytes + Qy_bytes
    
    # Convert the uncompressed public key to a human-readable format
    public_key_str = '0x' + binascii.hexlify(public_key_bytes).decode('utf-8')
    
    return public_key_str

def multiply(Gx, Gy, d):
    # Double-and-add algorithm for elliptic curve multiplication
    Qx = Gx
    Qy = Gy
    for i in range(255, -1, -1):
        Qx, Qy = double(Qx, Qy)
        if (d >> i) & 1:
            Qx, Qy = add(Qx, Qy, Gx, Gy)
    return Qx, Qy

def double(x, y):
    # Doubling formula for the secp256k1 curve
    s = (3 * x**2) * pow(2 * y, p-2, p)
    X = (s**2 - 2 * x) % p
    Y = (s * (x - X) - y) % p
    return X, Y

def add(x1, y1, x2, y2):
    # Addition formula for the secp256k1 curve
    s = (y2 - y1) * pow(x2 - x1, p-2, p)
    X = (s**2 - x1 - x2) % p
    Y = (s * (x1 - X) - y1) % p
    return X, Y

# Example usage: calculate public key from a private key
private_key = "e5c3cc3f0ccf8e2a15da062fa00c2b580f844a8f1d52d91c09f2145b5f5b5d7f"
public_key = get_public_key(private_key)
print("Public key:", public_key)
