#!/usr/bin/env python3
"""monsky.py uchun mutatsiya sinovi: formulaning har bir qismini buzamiz — test (monsky.py __main__) yiqilishi shart."""
import os, subprocess, sys, tempfile
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "monsky.py")).read()
MUT = [
 # EKVIVALENT (ushlanmaydi va ushlanishi shart emas): M_o da A+D2 <-> A+D-2 almashtirish = P M P, rang saqlanadi.
 ("M_o: diagonaldan tashqari D2 -> D-1", "M = blocks(add(A, D2), D2, D2, add(A, Dm2))", "M = blocks(add(A, D2), Dm1, D2, add(A, Dm2))"),
 ("a_ii nolga tenglangan", "A[i][i] = sum(A[i][j] for j in range(t) if j != i) % 2", "A[i][i] = 0"),
 ("juft n: D-1 o'rniga D-2", "M = blocks(D2, add(A, D2), add(AT, D2), Dm1)", "M = blocks(D2, add(A, D2), add(AT, D2), Dm2)"),
 ("2t o'rniga 2t-1", "return 2 * t - rank_f2(M)", "return 2 * t - 1 - rank_f2(M)"),
 ("Legendre teskari", "return 0 if pow(a % p, (p - 1) // 2, p) == 1 else 1", "return 1 if pow(a % p, (p - 1) // 2, p) == 1 else 0"),
 ("A transpozitsiyasiz (juft n)", "M = blocks(D2, add(A, D2), add(AT, D2), Dm1)", "M = blocks(D2, add(A, D2), add(A, D2), Dm1)"),
]
killed = 0
with tempfile.TemporaryDirectory() as d:
    for name, o, n in MUT:
        assert o in SRC, name
        open(os.path.join(d, "monsky.py"), "w").write(SRC.replace(o, n, 1))
        r = subprocess.run([sys.executable, "monsky.py"], cwd=d, capture_output=True, text=True, timeout=900)
        ok = r.returncode != 0
        killed += ok
        fails = [l.split("] ")[1][:2] for l in r.stdout.splitlines() if l.startswith("[FAIL]")]
        print(f"[{'KILLED' if ok else 'SURVIVED'}] {name:32s} yiqilgan testlar: {fails}")
print(f"\n{killed}/{len(MUT)} mutant ushlandi"); sys.exit(0 if killed == len(MUT) else 1)
