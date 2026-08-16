"""9x9 nonogram line solver with constraint propagation + DFS."""


def line_candidates(clue, n):
    """Yield all binary tuples of length n matching clue (list of run lengths)."""
    clue = [c for c in clue if c > 0]
    if not clue:
        yield (0,) * n
        return
    total = sum(clue) + len(clue) - 1
    if total > n:
        return

    def rec(pos, ci):
        if ci == len(clue):
            yield (0,) * (n - pos)
            return
        run = clue[ci]
        last = ci == len(clue) - 1
        max_start = n - (sum(clue[ci:]) + (len(clue) - ci - 1))
        for start in range(pos, max_start + 1):
            prefix = (0,) * (start - pos) + (1,) * run
            if last:
                yield prefix + (0,) * (n - start - run)
            else:
                for rest in rec(start + run + 1, ci + 1):
                    yield prefix + (0,) + rest

    yield from rec(0, 0)


def fits(cand, known):
    return all(k == -1 or k == c for k, c in zip(known, cand))


def solve(col_clues, row_clues, n=9, limit=2):
    """Return list of solutions (each grid[r][c]). col_clues[c], row_clues[r]."""
    rows_cands = [list(line_candidates(row_clues[r], n)) for r in range(n)]
    cols_cands = [list(line_candidates(col_clues[c], n)) for c in range(n)]
    if any(len(rc) == 0 for rc in rows_cands) or any(len(cc) == 0 for cc in cols_cands):
        return []

    grid = [[-1] * n for _ in range(n)]

    def propagate():
        changed = True
        while changed:
            changed = False
            for r in range(n):
                known = grid[r]
                cands = [c for c in rows_cands[r] if fits(c, known)]
                if not cands:
                    return False
                rows_cands[r] = cands
                for cidx in range(n):
                    vals = {c[cidx] for c in cands}
                    if len(vals) == 1:
                        v = next(iter(vals))
                        if grid[r][cidx] == -1:
                            grid[r][cidx] = v
                            changed = True
                        elif grid[r][cidx] != v:
                            return False
            for c in range(n):
                known = [grid[r][c] for r in range(n)]
                cands = [cc for cc in cols_cands[c] if fits(cc, known)]
                if not cands:
                    return False
                cols_cands[c] = cands
                for ridx in range(n):
                    vals = {cc[ridx] for cc in cands}
                    if len(vals) == 1:
                        v = next(iter(vals))
                        if grid[ridx][c] == -1:
                            grid[ridx][c] = v
                            changed = True
                        elif grid[ridx][c] != v:
                            return False
        return True

    if not propagate():
        return []

    sols = []

    def dfs():
        if len(sols) >= limit:
            return
        # find unknown cell
        target = None
        for r in range(n):
            for c in range(n):
                if grid[r][c] == -1:
                    target = (r, c)
                    break
            if target:
                break
        if target is None:
            sols.append([row[:] for row in grid])
            return
        r, c = target
        saved_g = [row[:] for row in grid]
        saved_rc = [list(x) for x in rows_cands]
        saved_cc = [list(x) for x in cols_cands]
        for v in (1, 0):
            grid[r][c] = v
            if propagate():
                dfs()
            # restore
            for i in range(n):
                grid[i] = saved_g[i][:]
            for i in range(n):
                rows_cands[i] = saved_rc[i][:]
                cols_cands[i] = saved_cc[i][:]
        # ensure grid restored for caller
        for i in range(n):
            grid[i] = saved_g[i][:]

    dfs()
    return sols


if __name__ == "__main__":
    import extract as E, geom as Geo
    import numpy as np
    from PIL import Image
    im = np.array(Image.open("map1.png").convert("RGB"))
    pts = E.dots(im)
    g = Geo.detect_grids(im)[0]
    x0, y0, cell = g["x0"], g["y0"], g["cell"]
    GRID = cell * 9
    cols, rows = [], []
    cz = [p for p in pts if x0 <= p[0] < x0 + GRID and y0 - 180 <= p[1] < y0 - 2]
    for c in range(9):
        cx0 = x0 + c * cell
        col = [p for p in cz if cx0 <= p[0] < cx0 + cell]
        ys = [p[1] for p in col]
        gs = E.split_gaps(ys, 18) if col else []
        gs.sort(key=lambda gg: min(ys[i] for i in gg)) if col else None
        cols.append([len(gg) for gg in gs])
    rz = [p for p in pts if x0 - 180 <= p[0] < x0 - 2 and y0 <= p[1] < y0 + GRID]
    for r in range(9):
        ry0 = y0 + r * cell
        row = [p for p in rz if ry0 <= p[1] < ry0 + cell]
        xs = [p[0] for p in row]
        gs = E.split_gaps(xs, 18) if row else []
        gs.sort(key=lambda gg: min(xs[i] for i in gg)) if row else None
        rows.append([len(gg) for gg in gs])
    print("cols", cols)
    print("rows", rows)
    sols = solve(cols, rows)
    print("solutions:", len(sols))
    if sols:
        for row in sols[0]:
            print("".join("#" if v else "." for v in row))
