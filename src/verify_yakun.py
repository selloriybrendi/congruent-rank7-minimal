#!/usr/bin/env python3
"""a(7) yakuniy tekshiruv (bitta chegara uchun). exit 0 = shu chegaragacha a(7) nomzodlari hammasi yo'qqa chiqdi.
Foydalanish: python3 verify_yakun.py N_KATTA N_KICHIK DIR_KATTA DIR_KICHIK GP_FAYL...
  1) pi_sanoq T(N_KATTA) = elak jami.txt T            (to'liqlik, mustaqil usul)
  2) elak nomzodlari k <= N_KICHIK = kichik elak nomzodlari (ikki yurish izchil)
  3) GP fayllar birlashmasi = elak nomzodlari to'plami  (har nomzod yo'qotishda qatnashgan)
  4) hamma GP qatorida r2 butun son va r2 < 7          (ERR yo'q, rang <= 6)
     --qoldiq FAYL: r2 >= 7 bo'lgan k uchun izogeniya sinfi bo'yicha eng kichik r2 (qoldiq.sh natijasi) qabul qilinadi"""
import subprocess
import sys


def nomzodlar(path, top=None):
    out = {}
    for ln in open(path):
        k, s = map(int, ln.split())
        if top is None or k <= top:
            out[k] = s
    return out


def main(a):
    qold = {}
    if "--qoldiq" in a:
        i = a.index("--qoldiq")
        for ln in open(a[i + 1]):
            k, r1, r2 = ln.split()
            qold[int(k)] = int(r2)
        a = a[:i] + a[i + 2:]
    nk, nm, dk, dm, gps = int(float(a[0])), int(float(a[1])), a[2], a[3], a[4:]
    R = []

    def check(name, ok, detail=""):
        R.append(bool(ok))
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  —  {detail}" if detail else ""))

    pi = subprocess.run(["./pi_sanoq", str(nk)], capture_output=True, text=True)
    tpi = int(next(ln for ln in pi.stdout.splitlines() if ln.startswith("T")).split()[1]) if pi.returncode == 0 else -1
    tel = int(next(ln for ln in open(f"{dk}/jami.txt") if ln.startswith("T")).split()[1])
    check(f"1 to'liqlik T({nk}): pi_sanoq = elak", tpi == tel, f"{tpi} = {tel}")

    big = nomzodlar(f"{dk}/nomzod.txt")
    small = nomzodlar(f"{dm}/nomzod.txt")
    check(f"2 izchillik: {dk} dagi k <= {nm} = {dm}", nomzodlar(f"{dk}/nomzod.txt", nm) == small, f"{len(small)} ta")

    rows = [ln.split() for g in gps for ln in open(g)]
    ks = [int(r[0]) for r in rows]
    check("3 qamrov: GP to'plami = elak nomzodlari (takrorsiz)", set(ks) == set(big) and len(ks) == len(set(ks)),
          f"{len(set(ks))} = {len(big)}")
    def r2_yakuniy(r):
        if not r[2].lstrip("-").isdigit():
            return None
        return min(int(r[2]), qold.get(int(r[0]), 99))
    bad = [r for r in rows if r2_yakuniy(r) is None or r2_yakuniy(r) >= 7]
    if qold:
        print(f"      (qoldiq: {sum(1 for r in rows if int(r[0]) in qold)} ta k izogeniya sinfi bilan qayta baholandi)")
    mx = max((r2_yakuniy(r) for r in rows if r2_yakuniy(r) is not None), default=None)
    check("4 hammasida r2 < 7 (ERR yo'q)", not bad, f"max r2 = {mx}; buzuq: {bad[:3]}")

    print(f"\n{sum(R)}/{len(R)} o'tdi")
    return 0 if all(R) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
