#!/usr/bin/env python3
"""DFS sanog'ining to'liqligi — mustaqil usul: numpy elagi bilan har k <= N uchun kvadratsizlik va toq tub
bo'luvchilar soni hisoblanadi (DFS ishlatilmaydi). Kutilgan: 1e6 -> 53964, 1e7 -> 788282 (C va Python DFS)."""
import sys
import numpy as np
from sympy import primerange
N = int(float(sys.argv[1]))
omega = np.zeros(N + 1, dtype=np.int8)
sqf = np.ones(N + 1, dtype=bool)
for p in primerange(3, N + 1):
    omega[p::p] += 1
    if p * p <= N:
        sqf[p * p::p * p] = False
sqf[4::4] = False                      # 4 | k  => kvadratsiz emas
sqf[0] = False
print(f"N={N:.0e}: kvadratsiz, toq tub bo'luvchilar >= 4: {int(np.count_nonzero(sqf & (omega >= 4)))}")
