#!/usr/bin/env python3
"""F1.2 · Monsky 2-Selmer rangi s(n) — kongruent son egri chizig'i E_n: y^2 = x^3 - n^2 x uchun.
Manba: Dujella–Janfada–Salami, J. Integer Seq. 12 (2009) 09.5.8, 3-bo'lim (Monsky 1994):
  n kvadratsiz, toq tub bo'luvchilari p_1..p_t.
  D_l = diag(d_i), d_i = 0 agar (l/p_i) = 1, aks holda 1   (l = -1, -2, 2)
  A = (a_ij): a_ij = 0 agar (p_j/p_i) = 1, aks holda 1 (j != i);  a_ii = sum_{j != i} a_ij  (F_2 da)
  s(n) = 2t - rank M_o (n toq),  M_o = [[A+D2, D2], [D2, A+D_{-2}]]
  s(n) = 2t - rank M_e (n juft), M_e = [[D2, A+D2], [A^T+D2, D_{-1}]]
  Teorema (Monsky): s(n) juft <=> n = 1, 2, 3 (mod 8).   r(n) <= s(n) <= 2t.
Tekshirish: python monsky.py   (exit 0 = hammasi o'tdi)"""
import sys

from sympy import factorint


def leg(a, p):
    """Legendre simvoli additiv ko'rinishda: 0 agar (a/p) = 1, 1 agar (a/p) = -1 (p toq tub, p ∤ a)."""
    return 0 if pow(a % p, (p - 1) // 2, p) == 1 else 1


def rank_f2(rows):
    """F_2 ustidagi matritsa rangi; qatorlar butun son bitmask ko'rinishida."""
    rows, r = list(rows), 0
    for bit in range(max((x.bit_length() for x in rows), default=0) - 1, -1, -1):
        piv = next((i for i in range(r, len(rows)) if rows[i] >> bit & 1), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> bit & 1:
                rows[i] ^= rows[r]
        r += 1
    return r


def s_from_primes(ps, even):
    """ps — n ning toq tub bo'luvchilari, even — 2 | n."""
    t = len(ps)
    if t == 0:
        return 0
    A = [[0] * t for _ in range(t)]
    for i, pi in enumerate(ps):
        for j, pj in enumerate(ps):
            if i != j:
                A[i][j] = leg(pj, pi)
        A[i][i] = sum(A[i][j] for j in range(t) if j != i) % 2
    D = {u: [leg(u, p) for p in ps] for u in (-1, -2, 2)}

    def blocks(tl, tr, bl, br):  # har blok t×t ro'yxat → 2t ta bitmask qator
        out = []
        for L, R in ((tl, tr), (bl, br)):
            for i in range(t):
                v = 0
                for j in range(t):
                    v |= (L[i][j] & 1) << (2 * t - 1 - j)
                    v |= (R[i][j] & 1) << (t - 1 - j)
                out.append(v)
        return out

    def diag(d):
        return [[d[i] if i == j else 0 for j in range(t)] for i in range(t)]

    def add(X, Y):
        return [[(X[i][j] + Y[i][j]) % 2 for j in range(t)] for i in range(t)]

    AT = [list(r) for r in zip(*A)]
    D2, Dm1, Dm2 = diag(D[2]), diag(D[-1]), diag(D[-2])
    if not even:
        M = blocks(add(A, D2), D2, D2, add(A, Dm2))
    else:
        M = blocks(D2, add(A, D2), add(AT, D2), Dm1)
    return 2 * t - rank_f2(M)


def s(n):
    f = factorint(n)
    assert all(e == 1 for e in f.values()), "n kvadratsiz bo'lishi kerak"
    return s_from_primes(sorted(p for p in f if p != 2), 2 in f)


if __name__ == "__main__":
    import cypari2
    pari = cypari2.Pari()
    ok_all = True

    def check(name, ok, detail=""):
        global ok_all
        ok_all &= bool(ok)
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  —  {detail}" if detail else ""))

    sq = [n for n in range(1, 20001) if all(e == 1 for e in factorint(n).values())]
    bad = [n for n in sq if (s(n) % 2 == 0) != (n % 8 in (1, 2, 3))]
    check(f"1 Monsky juftlik teoremasi: {len(sq)} ta kvadratsiz n <= 20000", not bad, f"buzilish: {bad[:5]}")

    worse, above, tested = [], 0, 0
    for n in sq[:1500]:
        E = pari.ellinit([0, 0, 0, -n * n, 0])
        r1, r2 = (int(x) for x in pari.ellrank(E)[:2])
        sn = s(n)
        tested += 1
        if r1 > sn or r2 > sn:
            worse.append((n, r1, r2, sn))
        above += sn > r2
    check(f"2 PARI: rang (r1 <= rank <= r2) hech qachon s(n) dan oshmaydi, birinchi {tested} kvadratsiz n",
          not worse, f"buzilish: {worse[:3]}; s(n) > r2 bo'lgan holatlar: {above} (Sha[2] yoki 2-izogeniya aniqroq)")

    A194687 = [1, 5, 34, 1254, 29274, 48272239, 6611719866, 797507543735]
    vals = [(r, k, s(k)) for r, k in enumerate(A194687)]
    check("3 A194687: har bir r uchun s(a(r)) >= r va juftlik mos (a(7) = 797507543735 — Rogers chegarasi)",
          all(sk >= r and (sk - r) % 2 == 0 for r, k, sk in vals), "  ".join(f"s({k})={sk}" for r, k, sk in vals))
    check("4 misollar: s(1)=0, s(5)=1, s(6)=1, s(34)=2", (s(1), s(5), s(6), s(34)) == (0, 1, 1, 2))
    sys.exit(0 if ok_all else 1)
