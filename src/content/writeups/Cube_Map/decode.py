"""Decode 3D-nonogram clues from a CUBE MAP puzzle png."""
import numpy as np
from PIL import Image
from scipy import ndimage

CELL = 54
NX = NY = 9
XLEFTS = [119, 776, 1433]
YTOPS = [209, 866, 1523]
GRID = 486


def dot_mask(im):
    r, g, b = im[:, :, 0].astype(int), im[:, :, 1].astype(int), im[:, :, 2].astype(int)
    return (r < 90) & (g > 170) & (b > 170)


def dot_units(area, w, h):
    """Classify a blob as N clue-dots (6x6 squares). Title strokes -> 0."""
    if 24 <= area <= 42 and 4 <= w <= 8 and 4 <= h <= 8:
        return 1
    if 50 <= area <= 78 and ((10 <= w <= 15 and 4 <= h <= 8) or
                             (4 <= w <= 8 and 10 <= h <= 15)):
        return 2
    if 80 <= area <= 112 and ((16 <= w <= 22 and 4 <= h <= 8) or
                              (4 <= w <= 8 and 16 <= h <= 22)):
        return 3
    return 0


def blobs(mask):
    lab, n = ndimage.label(mask)
    out = []
    objs = ndimage.find_objects(lab)
    for i, sl in enumerate(objs, start=1):
        if sl is None:
            continue
        ys, xs = np.where(lab[sl] == i)
        area = len(xs)
        if area < 12:
            continue
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        nd = dot_units(area, w, h)
        if nd == 0:
            continue
        cx = xs.mean() + sl[1].start
        cy = ys.mean() + sl[0].start
        out.append((cx, cy, nd))  # cx, cy, n_dots
    return out


def dots_in(blobs_list, x0, x1, y0, y1):
    """Return (cx,cy,ndots) for blobs whose centroid is in the box."""
    return [(cx, cy, nd) for (cx, cy, nd) in blobs_list
            if x0 <= cx < x1 and y0 <= cy < y1]


def cluster_1d(values, gap):
    """Cluster sorted scalar values; return list of (center, members_idx)."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    groups = []
    cur = [order[0]]
    for idx in order[1:]:
        if values[idx] - values[cur[-1]] > gap:
            groups.append(cur)
            cur = [idx]
        else:
            cur.append(idx)
    groups.append(cur)
    return groups


def col_clues(blobs_list, xleft, ytop):
    """Column clues: dots above grid. Returns list (len 9) of clue-number lists (top->bottom)."""
    pts = dots_in(blobs_list, xleft, xleft + GRID, ytop - 170, ytop - 2)
    clues = []
    for c in range(NX):
        cx0 = xleft + c * CELL
        cx1 = cx0 + CELL
        colpts = [(cx, cy, nd) for (cx, cy, nd) in pts if cx0 <= cx < cx1]
        if not colpts:
            clues.append([0])
            continue
        ys = [p[1] for p in colpts]
        groups = cluster_1d(ys, gap=26)  # glyph boxes separated vertically
        # order top->bottom
        groups_sorted = sorted(groups, key=lambda gp: min(ys[i] for i in gp))
        nums = [sum(colpts[i][2] for i in gp) for gp in groups_sorted]
        clues.append(nums)
    return clues


def row_clues(blobs_list, xleft, ytop):
    pts = dots_in(blobs_list, xleft - 170, xleft - 2, ytop, ytop + GRID)
    clues = []
    for r in range(NY):
        ry0 = ytop + r * CELL
        ry1 = ry0 + CELL
        rowpts = [(cx, cy, nd) for (cx, cy, nd) in pts if ry0 <= cy < ry1]
        if not rowpts:
            clues.append([0])
            continue
        xs = [p[0] for p in rowpts]
        groups = cluster_1d(xs, gap=26)
        groups_sorted = sorted(groups, key=lambda gp: min(xs[i] for i in gp))
        nums = [sum(rowpts[i][2] for i in gp) for gp in groups_sorted]
        clues.append(nums)
    return clues


def decode_layer(blobs_list, li):
    """li 0..8 -> grid position."""
    xleft = XLEFTS[li % 3]
    ytop = YTOPS[li // 3]
    return col_clues(blobs_list, xleft, ytop), row_clues(blobs_list, xleft, ytop)


if __name__ == "__main__":
    import sys
    fn = sys.argv[1] if len(sys.argv) > 1 else "map1.png"
    im = np.array(Image.open(fn).convert("RGB"))
    bl = blobs(dot_mask(im))
    print(f"{fn}: {len(bl)} blobs")
    cc, rc = decode_layer(bl, 0)
    print("z=1 COL clues (left->right):")
    for i, c in enumerate(cc):
        print(f"  col{i+1}: {c}")
    print("z=1 ROW clues (top->bottom):")
    for i, c in enumerate(rc):
        print(f"  row{i+1}: {c}")
