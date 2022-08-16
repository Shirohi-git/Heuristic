#!/usr/bin/python3
import sys


def main():
    res = sum(int(si.split()[2])for si in Score)
    print("\nSum =", res)
    return


if __name__ == "__main__":
    #Score = map(int, open(0).input().readlines()[::2])
    Score = sys.stdin.readlines()[::2]

    main()
