#!/usr/bin/env python3
"""a(7) loyihasi — bitta buyruq bilan tekshiruv (exit 0 = hammasi o'tdi). Og'ir hisoblarni emas, ularning to'g'riligini sinaydi.
Ishga tushirish: python3 verify_all.py (cypari2, numpy, sympy kerak)   (kongruent/ papkasidan)"""
import os
import subprocess
import sys

import cypari2
import numpy as np
from sympy import primerange

sys.path.insert(0, "faza1")
from monsky import s  # noqa: E402

pari = cypari2.Pari()
pari.allocatemem(2 * 10**9)
pari.default("nbthreads", 1)
R = []


def check(name, ok, detail=""):
    R.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  —  {detail}" if detail else ""))


def c_elak(N, lo=None):
    env = dict(os.environ)
    if lo is not None:
        env["ELAK_LO"] = str(lo)
    exe = "faza2/monsky_elak_lo" if lo is not None else "faza2/monsky_elak"
    out = subprocess.run([exe, str(N)], capture_output=True, text=True, env=env).stdout.splitlines()
    T = int(next(ln for ln in out if ln.startswith("T")).split()[1])
    C = sorted((int(ln.split()[1]), int(ln.split()[2])) for ln in out if ln.startswith("C"))
    H = {int(ln.split()[1]): int(ln.split()[2]) for ln in out if ln.startswith("H")}
    return T, C, H


def numpy_count(A, B):
    k = np.arange(A, B + 1, dtype=np.int64)
    rem = k.copy()
    om = np.zeros(k.size, dtype=np.int8)
    sqf = k % 4 != 0
    rem[rem % 2 == 0] //= 2
    for p in primerange(3, int(B ** 0.5) + 1):
        st = (-A) % p
        om[st::p] += 1
        rem[st::p] //= p
        if p * p <= B:
            sqf[(-A) % (p * p)::p * p] = False
    om[rem > 1] += 1
    return int(np.count_nonzero(sqf & (om >= 4)))


# 1. Monsky formulasi
A194687 = [1, 5, 34, 1254, 29274, 48272239, 6611719866, 797507543735]
check("1 s(a(r)) = r, r = 0..7 (A194687)", [s(k) for k in A194687] == list(range(8)))
check("2 Rathbun: s(51604646) = 5 (ikkinchi rang-5)", s(51604646) == 5)
sq = [n for n in range(1, 3001) if int(pari.issquarefree(n))]
check("3 Monsky juftlik teoremasi (n <= 3000)", all((s(n) % 2 == 0) == (n % 8 in (1, 2, 3)) for n in sq))

# 2. C elak = Python (faza1/nomzod_1e8.txt), to'liqlik numpy bilan
T8, C8, H8 = c_elak(10**8)
py8 = sorted(tuple(map(int, ln.split())) for ln in open("faza1/nomzod_1e8.txt"))
check("4 C elak 1e8 nomzodlari = Python (65 ta)", C8 == py8, f"{len(C8)} ta")
check("5 to'liqlik: C sanog'i 1e7 = numpy (DFS'siz)", c_elak(10**7)[0] == numpy_count(1, 10**7))
lo, hi = 999_000_000, 10**9
Tw = c_elak(hi, lo)[0]
check("6 chegara oynasi [9.99e8, 1e9]: C = numpy", Tw == numpy_count(lo, hi), f"{Tw}")
check("7 C elak 1e8: s(k) gistogrammasi yig'indisi = T", sum(H8.values()) == T8, f"T = {T8}")

# 3. Yo'qqa chiqarish natijalari (mavjud fayllar)
for f, n in (("faza2/gp_1e8.txt", 65), ("faza2/gp_1e9.txt", 2179), ("faza2/gp_1e10.txt", 47796)):
    rows = [ln.split() for ln in open(f)]
    check(f"8 {f}: {n} ta, hammasida r2 < 7", len(rows) == n and all(int(r[2]) < 7 for r in rows),
          f"max r2 = {max(int(r[2]) for r in rows)}")
nomz = set(int(ln.split()[0]) for ln in open("faza2/natija_1e10/nomzod.txt"))
gp10 = set(int(ln.split()[0]) for ln in open("faza2/gp_1e10.txt"))
check("9 1e10: har nomzod yo'qqa chiqarishda qatnashgan", nomz == gp10, f"{len(nomz)} = {len(gp10)}")

# 4. Sertifikat: a(7) nomzodi rang 7
k = 797507543735
E = pari.ellinit([0, 0, 0, -k * k, 0])
r = pari.ellrank(E, 4)
P = r[3]
reg = pari.matdet(pari.ellheightmatrix(E, P))
check("10 k = 797507543735: r1 = r2 = 7, 7 nuqta egri chiziqda, regulyator > 0",
      int(r[0]) == 7 and int(r[1]) == 7 and len(P) == 7 and all(int(pari.ellisoncurve(E, p)) for p in P) and float(reg) > 0,
      f"regulyator = {float(reg):.6g}")

# 5. Masala bayoni: E_{u^2 k} ≅ E_k (x = u^2 X, y = u^3 Y), demak eng kichik rang-7 k kvadratsiz — faqat kvadratsiz k ni elash yetarli
def mm(kk):
    return pari.ellminimalmodel(pari.ellinit([0, 0, 0, -kk * kk, 0]))[:5]


juft = [(3 + 7919 * t % 999983, 2 + t % 37) for t in range(40)]
check("11 E_(u^2 k) = E_k (40 juftlik, minimal model) va nazorat E_5 != E_6",
      all(mm(u * u * kk) == mm(kk) for kk, u in juft) and mm(5) != mm(6))

print(f"\n{sum(R)}/{len(R)} tekshiruv o'tdi")
sys.exit(0 if all(R) else 1)
