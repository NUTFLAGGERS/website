"""Extract per-layer clue digit bitmaps from a CUBE MAP png.

Each clue number is a 3x3 dot-matrix glyph. Column clues stack vertically above
each grid column; row clues run horizontally left of each grid row.
We segment each clue *line* by 1-D gaps along its axis so sparse glyphs
(corners/diagonals) stay intact.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

CELL = 54
XLEFTS = [119, 776, 1433]
YTOPS = [209, 866, 1523]
GRID = 486
PITCH = 8.6


def dots(im):
    r, g, b = im[:, :, 0].astype(int), im[:, :, 1].astype(int), im[:, :, 2].astype(int)
    # clue dots are green-cyan (0,230,240): B-G small. UI text "Z=N"/titles are
    # blue-cyan (0,212,255): B-G large. Filter to dots only.
    mask = (r < 90) & (g > 195) & (b > 195) & ((b - g) < 22)
    lab, n = ndimage.label(mask)
    objs = ndimage.find_objects(lab)
    pts = []
    for i, sl in enumerate(objs, 1):
        ys, xs = np.where(lab[sl] == i)
        area = len(xs)
        if area < 10:
            continue
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        # split merged dots (touching pair/triple) into individual dot centers
        cx0, cy0 = sl[1].start, sl[0].start
        nx = max(1, int(round(w / PITCH)))
        ny = max(1, int(round(h / PITCH)))
        if nx * ny == 1:
            pts.append((xs.mean() + cx0, ys.mean() + cy0))
        else:
            # distribute: cluster pixels into nx*ny cells
            for ix in range(nx):
                for iy in range(ny):
                    bx0 = cx0 + ix * w / nx
                    bx1 = cx0 + (ix + 1) * w / nx
                    by0 = cy0 + iy * h / ny
                    by1 = cy0 + (iy + 1) * h / ny
                    sel = [(x + cx0, y + cy0) for x, y in zip(xs, ys)
                           if bx0 <= x + cx0 < bx1 and by0 <= y + cy0 < by1]
                    if len(sel) >= 6:
                        mx = sum(p[0] for p in sel) / len(sel)
                        my = sum(p[1] for p in sel) / len(sel)
                        pts.append((mx, my))
    return pts


def split_gaps(vals, gap):
    """Return list of index-groups splitting sorted-by-val into runs with gaps>gap."""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    groups, cur = [], [order[0]]
    for idx in order[1:]:
        if vals[idx] - vals[cur[-1]] > gap:
            groups.append(cur)
            cur = [idx]
        else:
            cur.append(idx)
    groups.append(cur)
    return groups


def bitmap(pts_xy):
    xs = [p[0] for p in pts_xy]
    ys = [p[1] for p in pts_xy]
    x0, y0 = min(xs), min(ys)
    cells = set()
    for x, y in pts_xy:
        cells.add((round((x - x0) / PITCH), round((y - y0) / PITCH)))
    W = max(c[0] for c in cells) + 1
    H = max(c[1] for c in cells) + 1
    return tuple("".join("#" if (rx, ry) in cells else "." for rx in range(W))
                 for ry in range(H))


GAP = 18  # within-digit dot gap <=16, between-digit >=20


def layer_clues(pts, li, want="num"):
    """Return (cols, rows). want='num' -> clue numbers (dot counts);
    want='bmp' -> glyph bitmaps."""
    xl = XLEFTS[li % 3]
    yt = YTOPS[li // 3]
    cols, rows = [], []
    cz = [p for p in pts if xl <= p[0] < xl + GRID and yt - 170 <= p[1] < yt - 2]
    for c in range(9):
        cx0 = xl + c * CELL
        col = [p for p in cz if cx0 <= p[0] < cx0 + CELL]
        if not col:
            cols.append([])
            continue
        ys = [p[1] for p in col]
        groups = split_gaps(ys, GAP)
        groups.sort(key=lambda g: min(ys[i] for i in g))  # top->bottom
        if want == "num":
            cols.append([len(g) for g in groups])
        else:
            cols.append([bitmap([col[i] for i in g]) for g in groups])
    rz = [p for p in pts if xl - 170 <= p[0] < xl - 2 and yt <= p[1] < yt + GRID]
    for r in range(9):
        ry0 = yt + r * CELL
        row = [p for p in rz if ry0 <= p[1] < ry0 + CELL]
        if not row:
            rows.append([])
            continue
        xs = [p[0] for p in row]
        groups = split_gaps(xs, GAP)
        groups.sort(key=lambda g: min(xs[i] for i in g))  # left->right
        if want == "num":
            rows.append([len(g) for g in groups])
        else:
            rows.append([bitmap([row[i] for i in g]) for g in groups])
    return cols, rows


if __name__ == "__main__":
    from collections import Counter
    pat = Counter()
    for fn in [f"map{i}.png" for i in range(1, 10)]:
        im = np.array(Image.open(fn).convert("RGB"))
        pts = dots(im)
        for li in range(9):
            cols, rows = layer_clues(pts, li)
            for line in cols + rows:
                for g in line:
                    pat[g] += 1
    print("distinct patterns:", len(pat))
    for key, cnt in pat.most_common():
        nd = sum(r.count("#") for r in key)
        print(f"--- count={cnt} dots={nd} {len(key[0])}x{len(key)} ---")
        for r in key:
            print("  " + r)
