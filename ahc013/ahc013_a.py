#!/usr/bin/python3
import time


class Result:
    def __init__(self, moves, connects):
        self.moves = moves
        self.connects = connects
        self.print_answer()
        return

    def print_answer(self):
        print(len(self.moves))
        for arr in self.moves:
            print(*arr)
        print(len(self.connects))
        for arr in self.connects:
            print(*arr)
        return


class Grid:

    class Block:
        """
        num             : 番号(0~5)
        is_connected    : bool
        top, bottom, left, right    : 上下左右のPC座標, 番号
                                    上下:x 左右:y
        """

        def __init__(self, x, y, num=0, is_connected=0):
            self.INI = [(-1, -1), (N, N)]
            self.num = num
            self.xy = (x, y)
            self.is_connected = is_connected
            self.top, self.bottom = (-1, -1), (N, N)
            self.left, self.right = (-1, -1), (N, N)

            for i in range(x+1, N):
                if C[i][y] > 0:
                    self.bottom = (i, y)
                    break
            for i in range(x-1, -1, -1):
                if C[i][y] > 0:
                    self.top = (i, y)
                    break
            for j in range(y+1, N):
                if C[x][j] > 0:
                    self.right = (x, j)
                    break
            for j in range(y-1, -1, -1):
                if C[x][j] > 0:
                    self.left = (x, j)
                    break
            return

        def near(self):
            return [self.top, self.bottom, self.left, self.right]

    def __init__(self, key: int):
        self.key = key
        self.weight = ([16, 8, 4, 2, 1][-K:] * 2)[-K-(key-1):2*K-(key-1)]
        self.blocks = {}
        for i, ci in enumerate(C):
            for j, cij in enumerate(ci):
                self.blocks[(i, j)] = self.Block(i, j, cij)
        return

    def can_move(self, s: tuple, t: tuple) -> bool:
        blk_s = self.blocks[s]
        if s == t:
            return False
        if (blk_s.top[0] < t[0] < blk_s.bottom[0]
                and blk_s.left[1] < t[1] < blk_s.right[1]):
            return True
        return False

    def move_x(self, s: tuple, t: tuple):
        blocks = self.blocks

        # 移動先が範囲外 or どちらにも番号がついている -> False
        if s not in blocks or t not in blocks:
            return False
        if (blocks[s].num > 0) and (blocks[t].num > 0):
            return False

        bs, bt = blocks[s], blocks[t]
        bs.num, bt.num = bt.num, bs.num

        (sx, sy), (tx, ty) = s, t
        for j in range(max(bs.left[1], 0), s[1]+1):
            blocks[(sx, j)].right = bs.right
        for j in range(s[1], min(bs.right[1]+1, N)):
            blocks[(sx, j)].left = bs.left

        for j in range(max(bt.left[1], 0), t[1]):
            blocks[(tx, j)].right = t
        for j in range(t[1]+1, min(bt.right[1]+1, N)):
            blocks[(tx, j)].left = t

        top = min(bt.top, bs.top)
        btm = max(bt.bottom, bs.bottom)
        for i in range(max(top[0], 0), t[0]):
            blocks[(i, ty)].bottom = t
        for i in range(t[0], min(btm[0], N)):
            blocks[(i, ty)].bottom = btm
        for i in range(max(top[0]+1, 0), t[0]+1):
            blocks[(i, ty)].top = top
        for i in range(t[0]+1, min(btm[0]+1, N)):
            blocks[(i, ty)].top = t
        return True

    def move_y(self, s: tuple, t: tuple):
        blocks = self.blocks
        if s not in blocks or t not in blocks:
            return False
        if (blocks[s].num > 0) and (blocks[t].num > 0):
            return False

        bs, bt = blocks[s], blocks[t]
        bs.num, bt.num = bt.num, bs.num

        (sx, sy), (tx, ty) = s, t
        for i in range(max(bs.top[0], 0), s[0]+1):
            blocks[(i, sy)].bottom = bs.bottom
        for i in range(s[0], min(bs.bottom[0]+1, N)):
            blocks[(i, sy)].top = bs.top

        for i in range(max(bt.top[0], 0), t[0]):
            blocks[(i, ty)].bottom = t
        for i in range(t[0]+1, min(bt.bottom[0]+1, N)):
            blocks[(i, ty)].top = t

        lft = min(bt.left, bs.left)
        rht = max(bt.right, bs.right)
        for j in range(max(lft[1], 0), t[1]):
            blocks[(tx, j)].right = t
        for j in range(t[1], min(rht[1], N)):
            blocks[(tx, j)].right = rht
        for j in range(max(lft[1]+1, 0), t[1]+1):
            blocks[(tx, j)].left = lft
        for j in range(t[1]+1, min(rht[1]+1, N)):
            blocks[(tx, j)].left = t
        return True

    def move_straight(self, s: tuple, t: tuple):
        if s[0] != t[0]:
            res = self.move_x(s, t)
        else:  # elif s[1]!=t[1]:
            res = self.move_y(s, t)
        return res

    def move_cw(self, x, y) -> bool:
        return True

    def calc_dist(self, s: tuple, t: tuple) -> int:
        res = abs(s[0]-t[0]) + abs(s[1]-t[1])
        return res

    # return 評価値, 座標
    def calc_value(self, s: tuple, bfo=None) -> tuple:
        blk = self.blocks

        res = 0
        num = blk[s].num
        if bfo is not None:
            num = blk[bfo].num
        for dir in blk[s].near():
            if dir in blk[s].INI or dir == bfo:
                continue
            if num == blk[dir].num:
                res += 50 - self.calc_dist(s, dir)
        return res, s

    def calc_improve(self, s_calc: tuple, t: tuple) -> tuple:
        s_val, s = s_calc
        t_val, t = self.calc_value(t, bfo=s)
        if s == t or s_val == t_val:
            return 0, t
        t_val += min(s_val, 50)
        res = (t_val - s_val) // (self.calc_dist(s, t) // 5 + 1)
        res *= self.weight[self.blocks[s].num-1]
        return res, t


class Move:

    def __init__(self, grid: Grid):
        self.lim = K * 100
        self.grid = grid
        self.moves = []
        return

    def record_move_straight(self, s: tuple, t: tuple):
        if s[0] != t[0]:
            if s[0] < t[0]:
                rng = range(s[0], t[0]+1)
            else:  # elif s[0] > t[0]:
                rng = range(t[0], s[0]+1)[::-1]
            for r1, r2 in zip(rng, rng[1:]):
                self.moves.append((r1, s[1], r2, t[1]))
        else:  # elif s[1]!=t[1]:
            if s[1] < t[1]:
                rng = range(s[1], t[1]+1)
            else:  # elif s[1] > t[1]:
                rng = range(t[1], s[1]+1)[::-1]
            for r1, r2 in zip(rng, rng[1:]):
                self.moves.append((s[0], r1, t[0], r2))
        return

    def calc_dist(self, s: tuple, t: tuple) -> int:
        res = abs(s[0]-t[0]) + abs(s[1]-t[1])
        return res

    # ここ
    def solve_sparse(self, param: int):
        grid, blk = self.grid, self.grid.blocks
        self.lim_move = K * param  # パラメータ

        # return 更新差分, 更新前座標, 更新後座標
        def calc_improve_straight(s: tuple, c: int) -> tuple:
            bxy = blk[s]
            new, bfo = (0, s), grid.calc_value(s)
            col = [blk[lr].num for lr in [bxy.left, bxy.right] if lr in blk]
            if bxy.num not in col:
                for i in range(bxy.top[0], bxy.bottom[0])[1:]:
                    if self.calc_dist(bfo[1], (i, s[1])) > c:
                        continue
                    new = max(new, grid.calc_improve(bfo, (i, s[1])))

            row = [blk[tb].num for tb in [bxy.top, bxy.bottom] if tb in blk]
            if bxy.num not in row:
                for j in range(bxy.left[1], bxy.right[1])[1:]:
                    if self.calc_dist(bfo[1], (s[0], j)) > c:
                        continue
                    new = max(new, grid.calc_improve(bfo, (s[0], j)))
            return (-new[0], bfo[1], new[1])

        def max_improve(c: int):
            res = (0, (N, N), (N, N))
            for xy in blk.keys():
                if blk[xy].num != 0:
                    res = min(res, calc_improve_straight(xy, c))
            return res

        # ここ
        cnt_move = 0
        while cnt_move < self.lim_move:
            _, bfo, new = max_improve(self.lim_move - cnt_move)
            if grid.can_move(bfo, new):
                dist = self.calc_dist(bfo, new)
                if self.moves and self.moves[-1] == (*new, *bfo):
                    break
                elif cnt_move + dist < self.lim_move:
                    cnt_move += dist
                    self.record_move_straight(bfo, new)
                    _ = grid.move_straight(bfo, new)
                else:
                    break
            else:
                break

        self.lim_connect = self.lim - cnt_move
        return


class UnionFind:
    def __init__(self):
        self.parents = {}

    def find(self, x):
        if x not in self.parents:
            self.parents[x] = x
            return x
        elif self.parents[x] == x:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]

    def unite(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x != y:
            self.parents[x] = y


class Eval:
    USED = 9

    def __init__(self, blk, lim):
        self.c = [[blk[(i, j)].num for j in range(N)] for i in range(N)]
        self.lim_connect = lim
        self.connects = []
        return

    def calc_score(self):
        uf = UnionFind()
        for v in self.connects:
            i, j, i2, j2 = v
            p1 = (i, j)
            p2 = (i2, j2)
            assert 1 <= self.c_tmp[i][j] <= K
            assert 1 <= self.c_tmp[i2][j2] <= K
            uf.unite(p1, p2)

        computers = []
        for i in range(N):
            for j in range(N):
                if 1 <= self.c_tmp[i][j] <= K:
                    computers.append((i, j))

        score = 0
        for i in range(len(computers)):
            for j in range(i + 1, len(computers)):
                c1 = computers[i]
                c2 = computers[j]
                if uf.find(c1) != uf.find(c2):
                    continue

                if self.c_tmp[c1[0]][c1[1]] == self.c_tmp[c2[0]][c2[1]]:
                    score += 1
                else:
                    score -= 1
        self.score = max(score, 0)
        return

    def _solve_connect(self, permt: list):
        lim = self.lim_connect
        connects = []
        c_tmp = self.c_tmp = [ci[:] for ci in self.c]

        def can_connect(i, j, v):
            i2 = i + v[0]
            j2 = j + v[1]
            while i2 < N and j2 < N:
                if c_tmp[i2][j2] == 0:
                    i2 += v[0]
                    j2 += v[1]
                    continue
                elif c_tmp[i2][j2] == c_tmp[i][j]:
                    return True
                return False
            return False

        def do_connect(i, j, v):
            i2 = i + v[0]
            j2 = j + v[1]
            while i2 < N and j2 < N:
                if c_tmp[i2][j2] == 0:
                    c_tmp[i2][j2] = self.USED
                elif c_tmp[i2][j2] == c_tmp[i][j]:
                    connects.append([i, j, i2, j2])
                    return
                else:
                    raise AssertionError()
                i2 += v[0]
                j2 += v[1]

        for k in permt:
            for i in range(N):
                for j in range(N):
                    if c_tmp[i][j] != k:
                        continue
                    for v in [[0, 1], [1, 0]]:
                        if can_connect(i, j, v):
                            do_connect(i, j, v)
                            if len(connects) >= lim:
                                return connects
        return connects

    def solve_permutaiton(self, key: int):
        res = [*range(1, K+1)] * 2
        self.connects = self._solve_connect(res[key-1:key-1+K])
        return


def main():
    """
    ある番号だけを動かす
    ただし、隣接が同じ番号のときにはその軸から外れないように動く
    """
    s = time.time()
    res, val = 1, 0
    move, eval = [], []
    for k in range(1, K+1):
        move.append(Move(Grid(k)))
        move[k-1].solve_sparse(45)
        eval.append(Eval(move[k-1].grid.blocks, move[k-1].lim_connect))
        eval[k-1].solve_permutaiton(k), eval[k-1].calc_score()
        if val < eval[k-1].score:
            res, val = k, eval[k-1].score
        t = time.time()
        if TL - (t - s) < TL / 5:
            break
    Result(move[res-1].moves, eval[res-1].connects)
    return


if __name__ == "__main__":
    N, K = map(int, input().split())
    C = [list(map(int, input())) for _ in range(N)]
    TL = 2.7

    main()
