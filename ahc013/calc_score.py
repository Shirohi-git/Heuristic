#!/usr/bin/python3


class Result:
    def __init__(self, moves, connects):
        self.moves = moves
        self.connects = connects


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


def calc_score(res: Result):
    for v in res.moves:
        i, j, i2, j2 = v
        assert 1 <= C[i][j] <= K
        assert C[i2][j2] == 0
        C[i2][j2] = C[i][j]
        C[i][j] = 0

    uf = UnionFind()
    for v in res.connects:
        i, j, i2, j2 = v
        p1 = (i, j)
        p2 = (i2, j2)
        assert 1 <= C[i][j] <= K
        assert 1 <= C[i2][j2] <= K
        uf.unite(p1, p2)

    computers = []
    for i in range(N):
        for j in range(N):
            if 1 <= C[i][j] <= K:
                computers.append((i, j))

    score = 0
    for i in range(len(computers)):
        for j in range(i + 1, len(computers)):
            c1 = computers[i]
            c2 = computers[j]
            if uf.find(c1) != uf.find(c2):
                continue

            if C[c1[0]][c1[1]] == C[c2[0]][c2[1]]:
                score += 1
            else:
                score -= 1

    return max(score, 0)


if __name__ == "__main__":
    N, K = map(int, input().split())
    C = [list(map(int, input())) for _ in range(N)]

    X = int(input())
    MOVE = [list(map(int, input().split())) for _ in range(X)]
    Y = int(input())
    CNCT = [list(map(int, input().split())) for _ in range(Y)]

    res = Result(MOVE, CNCT)
    print(calc_score(res), K*100, X+Y, X, Y)
