from tokencrypt import _c_encrypt, TokenCrypt, _mat_inv_rows

# --- PASTE YOUR DATA FROM THE SERVER HERE ---
FLAG_CIPHERTEXT = [8542113, 3276882, 3690865, 7643264, 8105983, 1496901, 12888272, 11410520, 12905871, 11474255, 5852407, 10023987, 8271630]
PLAINTEXTS = [14292100, 397980, 11252192, 16641525, 4118042, 8573210, 1178201, 7924508, 1550218, 9183471, 14008272, 6092109, 305142, 15002133, 12728990, 8912301, 239401, 1049281, 7034189, 11092831, 550183, 16102938, 9283011, 1203912, 13490210, 2910381, 140291, 5910283, 8291023, 1510293, 1603912, 10293810, 1502938, 6910293, 1192039, 4920193, 1302910, 8910293, 5019283, 1592039]
CIPHERTEXTS = [8804300, 11048629, 14442596, 14279539, 13747536, 10704380, 8575457, 14735795, 8399414, 9771693, 7472783, 15504186, 7915368, 8429799, 15679626, 9463673, 7887989, 14032468, 7623435, 3832027, 16470716, 1648221, 8782008, 16616441, 9802885, 14450533, 7747769, 10465914, 15473048, 10784530, 3962501, 10938506, 6310747, 2915928, 7489064, 8657940, 2497024, 1084098, 11985903, 6021752]  # Paste the array you got from the `encrypt` command
# --------------------------------------------

def check_affine_and_extract_matrix(y_vals, c_vals):
    basis = [None] * 24
    for i in range(1, len(y_vals)):
        dy = y_vals[i] ^ y_vals[0]
        dc = c_vals[i] ^ c_vals[0]
        
        for bit in reversed(range(24)):
            if (dy >> bit) & 1:
                if basis[bit] is None:
                    basis[bit] = (dy, dc)
                    break
                else:
                    dy ^= basis[bit][0]
                    dc ^= basis[bit][1]
        else:
            if dc != 0: 
                return False, None # Not an affine mapping

    if any(b is None for b in basis):
        return False, None # Not enough linear independence

    def apply_M(x):
        out = 0
        for bit in reversed(range(24)):
            if (x >> bit) & 1:
                x ^= basis[bit][0]
                out ^= basis[bit][1]
        return out
        
    b = c_vals[0] ^ apply_M(y_vals[0])
    
    m_rows = []
    for r in range(24):
        row_val = 0
        for c in range(24):
            bit = (apply_M(1 << c) >> r) & 1
            row_val |= (bit << c)
        m_rows.append(row_val)
        
    return True, (m_rows, b)

print("Brute-forcing 16-bit Feistel key...")
for s in range(65536):
    # Calculate what the output of the Feistel network would be for this 's' guess
    y_vals = [_c_encrypt(pt, s, rounds=16) for pt in PLAINTEXTS]
    
    # Check if this guess cleanly maps to the ciphertexts via an affine transform
    is_affine, params = check_affine_and_extract_matrix(y_vals, CIPHERTEXTS)
    
    if is_affine:
        m_rows, b24 = params
        print(f"[+] Found key! s = {s}")
        
        # Reconstruct the exact cipher state locally
        ctx = TokenCrypt(0) 
        ctx._s = s
        ctx._m_rows = m_rows
        ctx._b24 = b24
        ctx._minv_rows = _mat_inv_rows(m_rows)
        
        # Decrypt the 1024-round flag using our cloned context
        decrypted_flag_tokens = [ctx.decrypt(c, rounds=1024) for c in FLAG_CIPHERTEXT]
        print(f"\n[+] Decrypted Token IDs: {decrypted_flag_tokens}")
        break
else:
    print("[-] Could not find the key. Did you copy the arrays correctly from the same session?")