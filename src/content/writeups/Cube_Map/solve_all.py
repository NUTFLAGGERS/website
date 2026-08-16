"""Solve all 9 cube-map puzzles and render projections."""
import numpy as np
from PIL import Image
import extract as E
import geom as Geo
import nonogram as N


def _contig_from_edge(groups, coords, edge_side):
    """groups: list of index-lists. coords: dict i->primary coord. Keep groups
    contiguous from the grid edge; stop at a gap > 45 (neighbor-clue contamination).
    edge_side='max' -> grid is at high coord (cols/rows: nearest digit has largest coord)."""
    centers = [(sum(coords[i] for i in g) / len(g), g) for g in groups]
    centers.sort(key=lambda t: t[0], reverse=(edge_side == "max"))
    kept = [centers[0][1]]
    prev = centers[0][0]
    for cen, g in centers[1:]:
        if abs(cen - prev) > 45:
            break
        kept.append(g)
        prev = cen
    return kept


def clues_for_grid(pts, g, margin=200):
    x0, y0, cell = g["x0"], g["y0"], g["cell"]
    GRID = cell * 9
    cols, rows = [], []
    cz = [p for p in pts if x0 <= p[0] < x0 + GRID and y0 - margin <= p[1] < y0 - 2]
    for c in range(9):
        cx0 = x0 + c * cell
        col = [p for p in cz if cx0 <= p[0] < cx0 + cell]
        if not col:
            cols.append([])
            continue
        ys = [p[1] for p in col]
        gs = E.split_gaps(ys, 18)
        gs = _contig_from_edge(gs, {i: ys[i] for i in range(len(ys))}, "max")
        gs.sort(key=lambda gg: min(ys[i] for i in gg))  # top->bottom
        cols.append([len(gg) for gg in gs])
    rz = [p for p in pts if x0 - margin <= p[0] < x0 - 2 and y0 <= p[1] < y0 + GRID]
    for r in range(9):
        ry0 = y0 + r * cell
        row = [p for p in rz if ry0 <= p[1] < ry0 + cell]
        if not row:
            rows.append([])
            continue
        xs = [p[0] for p in row]
        gs = E.split_gaps(xs, 18)
        gs = _contig_from_edge(gs, {i: xs[i] for i in range(len(xs))}, "max")
        gs.sort(key=lambda gg: min(xs[i] for i in gg))  # left->right
        rows.append([len(gg) for gg in gs])
    return cols, rows


def solve_map(mi):
    im = np.array(Image.open(f"map{mi}.png").convert("RGB"))
    pts = E.dots(im)
    grids = Geo.detect_grids(im)
    cube = np.zeros((9, 9, 9), dtype=int)  # [z][y][x]
    status = []
    for z, g in enumerate(grids):
        cols, rows = clues_for_grid(pts, g)
        sols = N.solve(cols, rows)
        if len(sols) == 1:
            cube[z] = np.array(sols[0])
            status.append("1")
        elif len(sols) > 1:
            cube[z] = np.array(sols[0])
            status.append(f"{len(sols)}")
        else:
            status.append("X")
    return cube, status


def render_layers(cube):
    out = []
    for z in range(9):
        out.append(f"z={z+1}")
        for r in range(9):
            out.append("  " + "".join("#" if cube[z][r][c] else "." for c in range(9)))
    return "\n".join(out)


if __name__ == "__main__":
    for mi in range(1, 10):
        cube, status = solve_map(mi)
        print(f"=== map{mi} layer status: {' '.join(status)} ===")
        np.save(f"cube{mi}.npy", cube)
    print("saved cubes")
