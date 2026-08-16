def dodeca_to_text(v_values, base=120):
    """
    Converts a list of dodecahedron V-values into a Base-27 text string.
    
    v_values: List of integers (0-119) representing each shape from left to right.
    base: The overflow threshold (116 based on your 'dl' discovery).
    """
    # 1. Calculate the Master Integer
    # We treat the list as a big-endian number (first shape is the most significant)
    master_integer = 0
    for i, v in enumerate(reversed(v_values)):
        master_integer += v * (base ** i)
    
    # 2. Convert Master Integer to Base-27
    # Alphabet: _=0, a=1, b=2 ... z=26
    alphabet = "_abcdefghijklmnopqrstuvwxyz"
    plaintext = []
    
    if master_integer == 0:
        return "_"
        
    temp_int = master_integer
    while temp_int > 0:
        remainder = temp_int % 27
        plaintext.append(alphabet[remainder])
        temp_int //= 27
        
    # Reverse to get the correct character order
    return "".join(reversed(plaintext))

# --- YOUR INPUT SECTION ---
# Enter the V-values for your 26 shapes here.
# Example: If your first shape is Set 22 with 1 rotation: V = (22-1)*5 + 1 = 106
my_v_values = [2, 114, 57, 45, 35, 45, 21, 83, 46, 106, 70, 33, 95, 37, 76, 119, 62, 82, 68, 111, 113, 91, 3, 19, 63, 106] # Replace this with your full list of 26 values

flag = dodeca_to_text(my_v_values)
print(f"Decoded Message: {flag}")


# master_integer = sum(v * (120**i) for i, v in enumerate(reversed(my_v_values)))

# # 2. Raw Byte Conversion (Base-256)
# # Find the length required
# byte_len = (master_integer.bit_length() + 7) // 8
# raw_bytes = master_integer.to_bytes(byte_len, byteorder='big')

# print(f"Option 1 (Big-Endian Raw Stream):\n{raw_bytes}")

# # 1. Reverse the List
# reversed_vs = my_v_values[::-1]

# # 2. Base-120 Positional Sum
# master_integer_rev = sum(v * (120**i) for i, v in enumerate(reversed(reversed_vs)))

# # 3. Raw Byte Conversion (Base-256)
# byte_len_rev = (master_integer_rev.bit_length() + 7) // 8
# raw_bytes_rev = master_integer_rev.to_bytes(byte_len_rev, byteorder='big')

# print(f"\nOption 2 (Little-Endian Raw Stream):\n{raw_bytes_rev}")