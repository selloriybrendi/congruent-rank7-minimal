# The smallest congruent number curve of rank seven

We prove that **a(7) = 797507543735** in [OEIS A194687](https://oeis.org/A194687): for every positive integer
k < 797507543735 the curve E_k : y² = x³ − k²x has rank at most 6, and E_797507543735 has rank 7 (Rogers).
Until now only the upper bound a(7) ≤ 797507543735 was known.

The proof is an exhaustive, unconditional computation (no GRH, BSD or parity conjecture):

1. **Monsky 2-Selmer sieve** (`src/monsky_elak.c`) over all squarefree k < 797507543735. A curve of rank ≥ 7 needs
   2-Selmer rank ≥ 7 (k ≡ 5, 6, 7 mod 8) or ≥ 8 (k ≡ 1, 2, 3 mod 8). Completeness: the sieve count
   T = 143452705272 equals an independent prime-counting count (`src/pi_sanoq.c`).
2. **Upper bounds** from PARI/GP `ellrank` (2-descent + Cassels pairing) for all 9053344 candidates.
3. **Isogeny refinement** (`src/qoldiq.sh`): the 163 candidates with r₂ ≥ 7 are re-bounded over their Q-isogeny class
   (rank is an isogeny invariant); every one drops to ≤ 5.
4. **Independent cross-check** with Cremona's `mwrank` (`src/mw_tekshir.py`): 866/866 (k ≤ 10¹¹) and 1788/1788
   (k > 10¹¹: all 785 candidates with r₂ ≥ 6, 1000 random ones, and a(5), a(6), a(7) as controls) agree.

- **Paper:** [`paper/a7.pdf`](paper/a7.pdf) (3 pages)
- **Certificate:** `data/` — candidate lists and per-k bounds (xz-compressed), residual table, logs

## Re-check the certificate (≈ 1 minute)

```bash
mkdir -p big small
xz -dc data/nomzod_797507543734.txt.xz > big/nomzod.txt && cp data/jami_797507543734.txt big/jami.txt
xz -dc data/nomzod_1e11.txt.xz > small/nomzod.txt && cp data/jami_1e11.txt small/jami.txt
xz -dc data/gp_1e11.txt.xz > gp_1e11.txt && xz -dc data/gp_yuqori.txt.xz > gp_yuqori.txt
cat data/gp_1e11.txt.qoldiq.natija data/gp_yuqori.txt.qoldiq.natija > qoldiq.txt
cc -O2 -o pi_sanoq src/pi_sanoq.c -lm && cp src/verify_yakun.py .
python3 verify_yakun.py 797507543734 1e11 big small gp_1e11.txt gp_yuqori.txt --qoldiq qoldiq.txt
```

Expected output: `4/4 o'tdi` (completeness, consistency, coverage 9053344 = 9053344, max r₂ = 6).
This checks the certificate; recomputing the bounds themselves needs PARI/GP 2.17 (`default(nbthreads,1)`) and
about a day on 10 cores (`src/yoqot_gp.sh`, `src/bo_ishla.sh`).

File formats: `nomzod_*.txt` — `k s(k)` (squarefree k and its 2-Selmer rank); `gp_*.txt` — `k r1 r2` (PARI `ellrank`
lower/upper bound); `*.qoldiq.natija` — `k r1max r2min` over the isogeny class.
Some comments and log lines are in Uzbek (`o'tdi` = passed, `nomzod` = candidate, `qoldiq` = residual).

## Cite

Kenjaev, O. U. (2026). *The smallest congruent number curve of rank seven* (v1.0). Zenodo.

## Use of generative AI

Claude Opus 5.5 (Anthropic, `claude-opus-5-5`) via Claude Code was used to write and run the programs and to help
prepare the text, under the author's direction; every number was produced by the programs and re-checked.
The author takes full responsibility.

## License

Code: MIT. Paper and data: CC BY 4.0. PARI/GP and eclib are separate programs and are not included.
