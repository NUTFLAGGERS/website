import struct, sys

MAGIC = 0xC4E71A59
VER = 0x21

def varint_decode(b, i):
    # big-endian, bit0 = continuation
    val = 0
    while True:
        byte = b[i]; i += 1
        val = (val << 7) | (byte >> 1)
        if (byte & 1) == 0:
            break
    return val, i

def varint_encode(v):
    if v == 0:
        return bytes([0])
    chunks = []
    while v > 0:
        chunks.append(v & 0x7f)
        v >>= 7
    chunks.reverse()
    out = bytearray()
    for idx, c in enumerate(chunks):
        cont = 1 if idx < len(chunks)-1 else 0
        out.append((c << 1) | cont)
    return bytes(out)

# collect all encoded string segments with their per-string positions
def collect_strings(b):
    segs = []  # list of (filepos, encbytes)
    i = 12  # skip header
    n = len(b)
    def parse(i):
        tag = b[i]; i += 1
        if tag == 0x02: return i
        if tag in (0x05,0x06): return i
        if tag == 0x23: return i+1
        if tag == 0x26: return i+2
        if tag == 0x2C: return i+4
        if tag == 0x29: return i+8
        if tag == 0x63:
            ln, i = varint_decode(b, i)
            segs.append((i, b[i:i+ln]))
            return i+ln
        if tag == 0x85:
            ln, i = varint_decode(b, i)
            return i+ln
        if tag == 0xA3:
            cnt, i = varint_decode(b, i)
            for _ in range(cnt): i = parse(i)
            return i
        if tag == 0xA6:
            cnt, i = varint_decode(b, i)
            for _ in range(cnt):
                i = parse(i); i = parse(i)
            return i
        if tag == 0xC3:
            i = parse(i)  # class name string
            i = parse(i)  # fields map
            return i
        if tag == 0xC9:
            return i+14
        raise ValueError(f"unknown tag 0x{tag:02x} at {i-1}")
    parse(i)
    return segs

KEY = b"gate"

def enc_str(s):
    if isinstance(s, str): s = s.encode()
    enc = bytes(s[i] ^ KEY[i % 4] for i in range(len(s)))
    return bytes([0x63]) + varint_encode(len(s)) + enc

def enc_int8(v):  return bytes([0x23]) + struct.pack(">b", v)
def enc_int16(v): return bytes([0x26]) + struct.pack(">h", v)
def enc_int32(v): return bytes([0x2C]) + struct.pack(">i", v)
def enc_int64(v): return bytes([0x29]) + struct.pack(">q", v)
def enc_null():   return bytes([0x02])
def enc_bool(v):  return bytes([0x05 if v else 0x06])
def enc_bytes(bb):return bytes([0x85]) + varint_encode(len(bb)) + bb

def enc_list(items):
    out = bytes([0xA3]) + varint_encode(len(items))
    for it in items: out += it
    return out

def enc_map(pairs):
    out = bytes([0xA6]) + varint_encode(len(pairs))
    for k, v in pairs: out += k + v
    return out

def enc_obj(classname, fields_map):
    return bytes([0xC3]) + enc_str(classname) + fields_map

def enc_call(name, args_list):
    # 0xe7: handler invocation -> [name string][args list]
    return bytes([0xe7]) + enc_str(name) + enc_list(args_list)

def enc_tcoord(epoch_us, dimension_id, stability):
    return bytes([0xC9]) + struct.pack(">q", epoch_us) + struct.pack(">i", dimension_id) + struct.pack(">h", stability)

# ---- full decoder (with key) for responses ----
def decode(b, i=12):
    tag = b[i]; i += 1
    if tag == 0x02: return None, i
    if tag == 0x05: return True, i
    if tag == 0x06: return False, i
    if tag == 0x23: return struct.unpack(">b", b[i:i+1])[0], i+1
    if tag == 0x26: return struct.unpack(">h", b[i:i+2])[0], i+2
    if tag == 0x2C: return struct.unpack(">i", b[i:i+4])[0], i+4
    if tag == 0x29: return struct.unpack(">q", b[i:i+8])[0], i+8
    if tag == 0x63:
        ln, i = varint_decode(b, i)
        raw = b[i:i+ln]; i += ln
        return bytes(raw[j] ^ KEY[j % 4] for j in range(ln)).decode('latin1'), i
    if tag == 0x85:
        ln, i = varint_decode(b, i)
        return b[i:i+ln], i+ln
    if tag == 0xA3:
        cnt, i = varint_decode(b, i)
        lst = []
        for _ in range(cnt):
            v, i = decode(b, i); lst.append(v)
        return lst, i
    if tag == 0xA6:
        cnt, i = varint_decode(b, i)
        d = {}
        for _ in range(cnt):
            k, i = decode(b, i); v, i = decode(b, i); d[k] = v
        return d, i
    if tag == 0xC3:
        name, i = decode(b, i); fields, i = decode(b, i)
        return {"__class__": name, **(fields if isinstance(fields, dict) else {"_": fields})}, i
    if tag == 0xe7:
        name, i = decode(b, i); args, i = decode(b, i)
        return {"__call__": name, "args": args}, i
    if tag == 0xC9:
        ep = struct.unpack(">q", b[i:i+8])[0]
        dim = struct.unpack(">i", b[i+8:i+12])[0]
        st = struct.unpack(">h", b[i+12:i+14])[0]
        return {"__tcoord__": True, "epoch_us": ep, "dimension_id": dim, "stability": st}, i+14
    return f"<unknown tag 0x{tag:02x}>", i

if __name__ == "__main__":
    b = open(sys.argv[1],"rb").read()
    print("magic", hex(struct.unpack(">I",b[0:4])[0]))
    print("ver", hex(b[4]), "flags", hex(b[5]))
    print("paylen", struct.unpack(">I",b[6:10])[0], "checksum", hex(struct.unpack(">H",b[10:12])[0]))
    segs = collect_strings(b)
    print("num strings", len(segs))
    # brute force per-string-reset 4-byte key requiring printable ASCII
    key = [None]*4
    for p in range(4):
        bestk, bestscore = 0, -1
        for k in range(256):
            score = 0; ok = True
            for (pos, enc) in segs:
                for idx in range(p, len(enc), 4):
                    c = enc[idx]^k
                    if 32 <= c < 127: score += 1
                    else: ok = False
            if ok and score > bestscore:
                bestscore = score; bestk = k
        key[p] = bestk
    print("key", [hex(k) for k in key])
    # decode all strings
    for (pos, enc) in segs:
        dec = bytes(enc[i]^key[i%4] for i in range(len(enc)))
        print(repr(dec.decode('latin1')))
