# 数学的ツール

## ceil(X/Y)

天井関数, Y < 1 で壊れる

## int_sqrt(X)

整数型 sqrt

## CRT(中国剰余定理)

    連立合同方程式
    x ≡ a1 (mod m1),
    x ≡ a2 (mod m2),
    　　　...
    x ≡ ak (mod mk)
    の解 x と その時の mod の値を返す。
    (解がないこともある。)

## Convolve_MOD(DFT, NTT, 離散フーリエ, 畳み込みなど)

MOD が特別なときに効果が強く発揮される。
ex 998244353 = 119 \* 2\*\*23 + 1, 原始根 = 3

### convolve(a, b)

    多項式乗算 の 係数 を返す。(NlogN where N = |a+b|)
    (a_0 + a_1 X^1 + ... + a_n X^n) * (...) =

形式的冪級数(ちゃんと理解はしてない) とか 組合せ とかで使えるがち。
n変数 は 係数を n重リストとかで保持(他にいい方法あるのでは?)
