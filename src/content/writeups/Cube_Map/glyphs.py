"""Cluster clue dots into glyphs and render as ASCII to identify the digit font."""
import numpy as np
from PIL import Image
from scipy import ndimage
import sys

CELL = 54
XLEFTS = [119, 776, 1433]
YTOPS = [209, 866, 1523]
GRID = 486
PITCH = 8.6


def dots(im):
    r, g, b = im[:, :, 0].astype(int), im[:, :, 1].astype(int), im[:, :, 2].astype(int)
    mask = (r < 90) & (g > 170) & (b > 170)
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
        cx = xs.mean() + sl[1].start
        cy = ys.mean() + sl[0].start
        pts.append((cx, cy, area, w, h))
    return pts


def cluster_glyphs(pts, dist=12.0):
    """Union-find clustering of dot centroids within `dist`."""
    n = len(pts)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        parent[find(a)] = find(b)

    for i in range(n):
        for j in range(i + 1, n):
            dx = pts[i][0] - pts[j][0]
            dy = pts[i][1] - pts[j][1]
            if dx * dx + dy * dy <= dist * dist:
                union(i, j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def render_glyph(pts, idxs):
    xs = [pts[i][0] for i in idxs]
    ys = [pts[i][1] for i in idxs]
    x0, y0 = min(xs), min(ys)
    cells = set()
    for i in idxs:
        cx = round((pts[i][0] - x0) / PITCH)
        cy = round((pts[i][1] - y0) / PITCH)
        cells.add((cx, cy))
    W = max(c[0] for c in cells) + 1
    H = max(c[1] for c in cells) + 1
    rows = []
    for ry in range(H):
        rows.append("".join("#" if (rx, ry) in cells else "." for rx in range(W)))
    return rows, len(idxs), (x0, y0, W, H)


def zone_for(li, kind):
    xl = XLEFTS[li % 3]
    yt = YTOPS[li // 3]
    if kind == "col":
        return (xl, xl + GRID, yt - 170, yt - 2)
    else:
        return (xl - 170, xl - 2, yt, yt + GRID)


if __name__ == "__main__":
    fn = sys.argv[1] if len(sys.argv) > 1 else "map1.png"
    li = int(sys.argv[2]) if len(sys.argv) > 2 else 2  # default z=3
    kind = sys.argv[3] if len(sys.argv) > 3 else "col"
    im = np.array(Image.open(fn).convert("RGB"))
    pts = dots(im)
    x0, x1, y0, y1 = zone_for(li, kind)
    zpts = [(p, i) for i, p in enumerate(pts) if x0 <= p[0] < x1 and y0 <= p[1] < y1]
    sub = [p for p, i in zpts]
    groups = cluster_glyphs(sub)
    glyphs = []
    for g in groups:
        rows, ndots, (gx, gy, W, H) = render_glyph(sub, g)
        glyphs.append((gx, gy, rows, ndots, W, H))
    # order by position: cols left->right then top->bottom; rows top->bottom then left->right
    glyphs.sort(key=lambda t: (round(t[0] / 30), t[1]) if kind == "col" else (round(t[1] / 30), t[0]))
    print(f"{fn} z={li+1} {kind} clues — {len(glyphs)} glyphs")
    for gx, gy, rows, ndots, W, H in glyphs:
        print(f"  @x={gx:.0f} y={gy:.0f} dots={ndots} {W}x{H}")
        for r in rows:
            print("      " + r)
