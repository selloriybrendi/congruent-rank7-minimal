#!/usr/bin/env python3
"""Ikkinchi mustaqil dastur (AI-dars #24): PARI ellrank natijalarini Cremona mwrank (eclib) bilan qayta tekshirish.
Foydalanish: ../.venv-eclib/bin/python mw_tekshir.py GP_FAYL N_TASODIFIY [P=3] [QOLDIQ_FAYL]
  tanlov: N ta tasodifiy + r2 >= MW_R2 (standart 6) bo'lgan hammasi + nazorat a(5), a(6), a(7)
  har qator: "k pari_r1 pari_r2 mw_rank mw_bound certain soniya"
  O'TISH sharti: har k uchun min(pari_r2, qoldiq_r2, mw_bound) < 7 (a(7) dan tashqari) va pari_r1 <= mw_bound, mw_rank <= pari_r2
  (ikki dastur bir-biriga zid kelmasin)."""
import random
import sys
import time
from multiprocessing import Pool


def mw(k):
    from sage.libs.eclib.interface import mwrank_EllipticCurve
    t = time.time()
    E = mwrank_EllipticCurve([0, 0, 0, -k * k, 0])
    return k, int(E.rank()), int(E.rank_bound()), bool(E.certain()), round(time.time() - t, 2)


def main(a):
    gp, n, p = a[0], int(a[1]), int(a[2]) if len(a) > 2 else 3
    qold = {int(ln.split()[0]): int(ln.split()[2]) for ln in open(a[3])} if len(a) > 3 else {}
    rows = {int(r[0]): (int(r[1]), int(r[2])) for r in (ln.split() for ln in open(gp))}
    random.seed(20260928)
    chegara = int(__import__("os").environ.get("MW_R2", "6"))  # 1e11 da r2>=5 (843); yuqori oraliqda r2>=5 = 231676 → ~122 soat, shuning uchun r2>=6
    tanlov = set(random.sample(sorted(rows), min(n, len(rows)))) | {k for k, (_, r2) in rows.items() if r2 >= chegara}
    nazorat = {48272239: (5, 5), 6611719866: (6, 6), 797507543735: (7, 7)}
    ish = sorted(tanlov) + sorted(nazorat)
    print(f"tanlov: {len(tanlov)} ta (r2>={chegara} hammasi: {sum(1 for k in tanlov if rows[k][1] >= chegara)}) + nazorat {len(nazorat)}", flush=True)
    bad, n_ok = [], 0
    with Pool(p) as pool:
        for k, mr, mb, cert, dt in pool.imap_unordered(mw, ish):
            r1, r2 = rows.get(k, nazorat.get(k))
            zid = r1 > mb or mr > r2
            yakun = min(r2, qold.get(k, 99), mb)
            if k in nazorat:
                ok = (mr, mb) == nazorat[k] and not zid
                print(f"NAZORAT {k} {r1} {r2} {mr} {mb} {cert} {dt}  {'OK' if ok else 'XATO'}", flush=True)
            else:
                ok = yakun < 7 and not zid
            if ok:
                n_ok += 1
            else:
                bad.append((k, r1, r2, mr, mb, cert))
    print(f"\n{n_ok}/{len(ish)} mos · zid yoki r>=7: {bad[:10]}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
