#!/usr/bin/python3
# 色TSP 形色毎TSP 
# ハンガー数より多い形 は 頂点を増やし、H-ハンガー が頂点間距離

# 次やりたいこと
# 色ごとにTSP ハンガー数より多いもの は 頂点を増やし、H-ハンガー が頂点間距離

class TSP:
    def __init__(self, n, dist):
        self.n = n
        self.log2 = {pow(2, i): i for i in range(n)}
        self.memo = [[-1] * (1 << n) for _ in range(n)]
        self.dist = [di[:] for di in dist]
        self.bfo = [-1] * (1 << n)
        self.bfo[-1] = 's'

        self.tspdp()

    def tspdp(self, s=0, bit=1):
        if bit == (1 << self.n) - 1:
            self.memo[s][bit] = self.dist[s][0]
            return self.dist[s][0]

        res = float('inf')
        for t in range(self.n):
            if (bit >> t) & 1:
                continue
            nxt = bit + (1 << t)
            if self.memo[t][bit] == -1:
                self.memo[t][bit] = self.tspdp(t, nxt)
            tmp = self.dist[s][t] + self.memo[t][bit]
            if tmp < res:
                res = min(res, tmp)
                self.bfo[bit] = nxt
        return res

    def route(self):
        res = [self.log2[1], 1]
        while self.bfo[res[-1]] != 's':
            nxt = self.bfo[res[-1]]
            bfo = res.pop()
            res.append(self.log2[nxt ^ bfo])
            res.append(nxt)
        res = res[-2::-1] * 2
        idx = max(range(1, self.n+1),
                  key=lambda x: self.dist[res[x-1]][res[x]])
        return res[idx: idx+self.n]


class Hook:
    def __init__(self, h, k, n):
        self.now = [-1] * h
        self.cnt = k[:]
        self.will_make = [ni[:] for ni in n]
        self.bfo = (-1, -1, -1)
        return

    def get_idx(self, num):
        return num % H

    def collect(self, idx):
        idx = self.get_idx(idx)
        shp = self.now[idx]
        if shp >= 0:
            self.cnt[shp] += 1
        self.now[idx] = -1
        return (-1 if shp >= 0 else -2)

    def attach(self, idx, shp, col):
        idx = self.get_idx(idx)
        self.cnt[shp] -= 1
        self.now[idx] = shp
        self.will_make[shp][col] -= 1
        return (shp, col, 0)

    def can_replace(self, idx, b_shp, b_col, b_cnt, n_shp, n_col):
        idx = self.get_idx(idx)
        if self.will_make[n_shp][n_col] <= 0:
            return False
        if self.cnt[n_shp] + (self.now[idx] == n_shp) <= 0:
            return False
        if b_shp == -1:
            return True
        if b_cnt < max(A[b_shp][n_shp], B[b_col][n_col]):
            return False
        return True

    def replace(self, idx, nxt):
        res = (self.collect(idx),)

        if self.can_replace(idx, *self.bfo, *nxt):
            self.bfo = self.attach(idx, *nxt)
            res = nxt[:]
            res = (res[0]+1, res[1]+1)
        else:
            *bfo_shpcol, bfo_cnt = self.bfo
            self.bfo = (*bfo_shpcol, bfo_cnt+1)
        return res


class Priority:
    def __init__(self):
        self.c_route = TSP(C, B).route() * 2
        self.s_route = TSP(S, A).route() * 2

    def color(self):  # 空フックを減らしたいとき
        pass

    def shape(self):  # ハンガー交換を減らしたいとき
        pass

    def query(self):
        que = []
        for j in self.c_route:
            for i in self.s_route:
                que += [(i, j)] * N[i][j]
        return que[::-1]


def main():
    prio = Priority()
    hook = Hook(H, K, N)

    id = 0
    ans = []
    for ci in prio.c_route:
        while sum(hook.will_make[si][ci] for si in range(S)) > 0:
            nxt = (0, ci)
            s_id = 0
            if hook.bfo[0] in prio.s_route:
                s_id = prio.s_route.index(hook.bfo[0])
            for si in prio.s_route[s_id:]:
                if hook.can_replace(id, *hook.bfo, *(si, ci)):
                    nxt = (si, ci)
                    break
            res = hook.replace(id, nxt)
            id += 1
            ans.append(res)

    print(len(ans))
    for ai in ans:
        print(*ai)
    return


if __name__ == '__main__':
    S, C, H, a, b = map(int, input().split())
    N = [list(map(int, input().split())) for _ in range(S)]
    K = list(map(int, input().split()))
    A = [list(map(int, input().split())) for _ in range(S)]
    B = [list(map(int, input().split())) for _ in range(C)]

    main()
