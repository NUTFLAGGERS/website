import struct, subprocess, tsp, sys

URL = "https://cddc2026.xyz:5007/api/temporal/compute"

def checksum(payload):
    s = 0
    for i, byte in enumerate(payload):
        s = (s + byte * ((i % 255) + 1)) & 0xFFFF
    return s ^ 0xA55A

def frame(payload, flags=0x00):
    return struct.pack(">IBBIH", tsp.MAGIC, tsp.VER, flags, len(payload), checksum(payload)) + payload

def send_raw(data):
    open("req.bin","wb").write(data)
    out = subprocess.run(["curl","-sk","-D","-","-X","POST",URL,
        "-H","Content-Type: application/x-tsp",
        "--data-binary","@req.bin","--max-time","20"], capture_output=True)
    raw = out.stdout
    # split headers/body
    sep = raw.find(b"\r\n\r\n")
    headers = raw[:sep].decode('latin1') if sep>=0 else raw.decode('latin1','replace')
    body = raw[sep+4:] if sep>=0 else b""
    return headers, body

def build_query(params_pairs, epoch_us=1700000000000000, dim=1, stab=100, flags=0x00):
    ts = tsp.enc_tcoord(epoch_us, dim, stab)
    fields = tsp.enc_map([
        (tsp.enc_str("timestamp"), ts),
        (tsp.enc_str("parameters"), tsp.enc_map(params_pairs)),
    ])
    payload = tsp.enc_obj("TemporalQuery", fields)
    return frame(payload, flags)

def show(headers, body):
    print(headers.split("\r\n")[0])
    ct = ""
    for h in headers.split("\r\n"):
        if h.lower().startswith("content-type"): ct = h
        if h.lower().startswith("x-tsp"): print(h)
    print(ct)
    if "json" in ct.lower():
        print(body.decode('latin1'))
    else:
        print("BODY HEX:", body.hex())
        try:
            val, _ = tsp.decode(body, 12)
            import pprint; pprint.pprint(val)
        except Exception as e:
            print("decode err", e)

if __name__ == "__main__":
    params = [
        (tsp.enc_str("dimension"), tsp.enc_str("alpha")),
        (tsp.enc_str("depth"), tsp.enc_int32(42)),
    ]
    flags = int(sys.argv[1],16) if len(sys.argv)>1 else 0x00
    h, b = send_raw(build_query(params, flags=flags))
    show(h, b)
