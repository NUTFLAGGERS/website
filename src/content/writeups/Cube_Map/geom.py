"""Auto-detect grid geometry (positions, cell size) for a CUBE MAP png.

Each map has a 3x3 arrangement of 9x9 nonogram grids. Grids in the same
column share vertical line x-positions; same row share horizontal y-positions.
"""
import numpy as np
from PIL import Image
from scipy import ndimage


def gridline_mask(im):
    r, g, b = im[:, :, 0].astype(int), im[:, :, 1].astype(int), im[:, :, 2].astype(int)
    # gridline ~ (44,69,107): bluish, brighter than cell bg (13,27,48), b>g>r
    return (r > 28) & (r < 80) & (g > 42) & (g < 100) & (b > 72) & (b < 150) & (b > g) & (g > r)


def line_positions(proj, min_frac=0.30):
    th = proj.max() * min_frac
    idx = np.where(proj > th)[0]
    groups = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i - p > 8:
                groups.append((s + p) // 2)
                s = i
            p = i
        groups.append((s + p) // 2)
    return groups


def equal_runs(lines, n=10, tol=0.18):
    """Find runs of `n` lines with near-constant spacing. Return list of (start,step)."""
    lines = sorted(lines)
    runs = []
    i = 0
    L = len(lines)
    while i < L:
        # try to extend a run of constant step starting at i
        if i + 1 >= L:
            break
        step = lines[i + 1] - lines[i]
        run = [lines[i], lines[i + 1]]
        j = i + 2
        while j < L and abs((lines[j] - run[-1]) - step) <= step * tol:
            run.append(lines[j])
            j += 1
        if len(run) >= n - 1:  # ~10 lines
            runs.append((run[0], step, len(run)))
            i = j
        else:
            i += 1
    return runs


def detect_grids(im, ncells=9):
    """Find grids as connected gridline-mesh components.
    Returns list of dicts {x0,y0,cell,n} ordered z=1..9 (reading order)."""
    gl = gridline_mask(im)
    gl = ndimage.binary_dilation(gl, iterations=2)
    lab, n = ndimage.label(gl)
    objs = ndimage.find_objects(lab)
    grids = []
    for i, sl in enumerate(objs, 1):
        y0, y1 = sl[0].start, sl[0].stop
        x0, x1 = sl[1].start, sl[1].stop
        w, h = x1 - x0, y1 - y0
        if w < 120 or h < 120:
            continue
        if abs(w - h) > 0.25 * max(w, h):  # roughly square
            continue
        area = (lab[sl] == i).sum()
        if area < 0.05 * w * h:  # must be a mesh, not a blob
            continue
        # account for the 2px dilation
        gx0, gy0 = x0 + 2, y0 + 2
        gw, gh = w - 4, h - 4
        cell = (gw + gh) / 2 / ncells
        grids.append({"x0": gx0, "y0": gy0, "x1": gx0 + gw, "y1": gy0 + gh,
                      "cell": cell, "n": ncells})
    # refine each grid's exact border lines from the gridline projection
    for g in grids:
        refine(gl, g)
    # order reading order: group by row (y) then col (x)
    grids.sort(key=lambda g: (round(g["y0"] / 100), g["x0"]))
    return grids


def refine(gl, g, ncells=9):
    """Refine x0,y0,cell using precise line positions inside the grid bbox."""
    m = 8
    sub = gl[max(0, g["y0"] - m):g["y1"] + m, max(0, g["x0"] - m):g["x1"] + m]
    ox = max(0, g["x0"] - m)
    oy = max(0, g["y0"] - m)
    vx = line_positions(sub.sum(axis=0), 0.45)
    hy = line_positions(sub.sum(axis=1), 0.45)
    if len(vx) >= 2:
        g["x0"] = vx[0] + ox
        g["cellx"] = (vx[-1] - vx[0]) / (len(vx) - 1)
    if len(hy) >= 2:
        g["y0"] = hy[0] + oy
        g["celly"] = (hy[-1] - hy[0]) / (len(hy) - 1)
    g["cell"] = (g.get("cellx", g["cell"]) + g.get("celly", g["cell"])) / 2


if __name__ == "__main__":
    for i in range(1, 10):
        im = np.array(Image.open(f"map{i}.png").convert("RGB"))
        gs = detect_grids(im)
        print(f"map{i}: {len(gs)} grids, cell~{np.median([g['cell'] for g in gs]):.1f}")
        for z, g in enumerate(gs, 1):
            print(f"   z={z}: x0={g['x0']} y0={g['y0']} cell={g['cell']:.1f}")
