import random
import tkinter as tk
from tkinter import filedialog



def decompress_file():
    # Open file dialog to choose file to decompress
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # Read compressed data from file
    with open(file_path, "rb") as f:
        compressed_data = f.read()

    # Decompress data
    data = decompress_data(compressed_data)

    # Open file dialog to choose save location for decompressed data
    save_path = filedialog.asksaveasfilename()

    # Write decompressed data to file
    with open(save_path, "wb") as f:
        f.write(data)


def compress_file():
    # Open file dialog to choose file to compress
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # Read contents of file
    with open(file_path, "rb") as f:
        data = f.read()

    # Find seed that generates the most efficient compressed data
    best_seed = None
    best_compressed_data = None
    min_compressed_size = float("inf")
    for seed in range(2**32):
        compressed_data = compress_data(data, seed)
        compressed_size = len(compressed_data)
        if compressed_size < min_compressed_size:
            best_seed = seed
            best_compressed_data = compressed_data
            min_compressed_size = compressed_size

    # Open file dialog to choose save location for compressed data
    save_path = filedialog.asksaveasfilename()

    # Write compressed data and seed to file
    with open(save_path, "wb") as f:
        f.write(best_seed.to_bytes(4, byteorder="big"))
        f.write(best_compressed_data)

def decompress_data(compressed_data):
    seed = int.from_bytes(compressed_data[:4], byteorder="big")
    compressed_data = compressed_data[4:]
    random.seed(seed)
    target_data = bytearray(len(compressed_data) // 5)
    for i in range(0, len(compressed_data), 5):
        byte = int.from_bytes(compressed_data[i:i+1], byteorder="big")
        index = int.from_bytes(compressed_data[i+1:i+5], byteorder="big")
        target_data[index] = byte
    return bytes(target_data)

def compress_data(data, seed):
    # Set random seed
    random.seed(seed)

    # XOR data with random bytes and store parity bits
    compressed_data = bytearray()
    for byte in data:
        random_byte = random.randint(0, 255)
        compressed_data.append(byte ^ random_byte)
        compressed_data.append((byte ^ random_byte) % 2)

    return bytes(compressed_data)

# Example usage
compress_file()
decompress_file()
