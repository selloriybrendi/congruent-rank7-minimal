/* monsky_elak.c — a(7) nomzodlari elagi (C).  Kvadratsiz k <= N, toq tub bo'luvchilar soni t >= 4.
 * s(k) — Monsky 2-Selmer rangi (Dujella–Janfada–Salami 2009, 3-bo'lim):
 *   toq k:  M_o = [[A+D2, D2], [D2, A+D_{-2}]],  juft k (k = 2·p1..pt):  M_e = [[D2, A+D2], [A^T+D2, D_{-1}]],
 *   s = 2t - rank_F2(M).
 * Nomzod: s >= 7 (k = 5,6,7 mod 8) yoki s >= 8 (k = 1,2,3 mod 8).
 * Foydalanish: ./monsky_elak N [shard nshard]   → "C k s" qatorlari + "H s soni" gistogramma + "T jami"
 * Ish taqsimoti: (1-tub indeksi, 2-tub indeksi) juftligi bo'yicha shard = (i1*1000003 + i2) % nshard.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned long long u64;
typedef unsigned __int128 u128;

static u64 N, M;            /* M = N / 105: eng katta tub bo'luvchi chegarasi (3·5·7 = 105) */
static uint8_t *comp;       /* toq sonlar uchun murakkablik bitseti: indeks = (x-1)/2 */
static int SH = 0, NSH = 1;
static u64 hist[64], total = 0;

static inline int is_prime_odd(u64 x) { return !(comp[(x - 1) >> 4] >> (((x - 1) >> 1) & 7) & 1); }
static inline void set_comp(u64 x) { comp[(x - 1) >> 4] |= (uint8_t)(1u << (((x - 1) >> 1) & 7)); }

static void sieve(void) {
    u64 nb = ((M - 1) >> 4) + 1;
    comp = calloc(nb + 1, 1);
    if (!comp) { fprintf(stderr, "xotira yetmadi\n"); exit(1); }
    set_comp(1);
    for (u64 p = 3; p * p <= M; p += 2)
        if (is_prime_odd(p))
            for (u64 q = p * p; q <= M; q += 2 * p) set_comp(q);
}

/* Jacobi simvoli (a/n), n toq musbat; additiv qaytaradi: 0 -> +1, 1 -> -1 (a, n o'zaro tub bo'lishi shart) */
static inline int jac(u64 a, u64 n) {
    int r = 0;
    a %= n;
    while (a) {
        while (!(a & 1)) { a >>= 1; if ((n & 7) == 3 || (n & 7) == 5) r ^= 1; }
        u64 t = a; a = n; n = t;
        if ((a & 3) == 3 && (n & 3) == 3) r ^= 1;
        a %= n;
    }
    return r;
}

static int t;                   /* joriy toq tublar soni */
static u64 ps[32];
static uint8_t L[32][32];       /* L[i][j] = (p_j / p_i) additiv */
static uint8_t Dm1[32], D2[32], Dm2[32];

static int rank_rows(uint32_t *rows, int n) {
    uint32_t basis[32] = {0};
    int r = 0;
    for (int i = 0; i < n; i++) {
        uint32_t v = rows[i];
        for (int b = 31; b >= 0 && v; b--) {
            if (!(v >> b & 1)) continue;
            if (!basis[b]) { basis[b] = v; r++; v = 0; break; }
            v ^= basis[b];
        }
    }
    return r;
}

static int monsky_s(int even) {
    uint8_t A[32][32];
    for (int i = 0; i < t; i++) {
        int d = 0;
        for (int j = 0; j < t; j++) if (j != i) { A[i][j] = L[i][j]; d ^= L[i][j]; }
        A[i][i] = (uint8_t)d;
    }
    uint32_t rows[64];
    int T2 = 2 * t;
    for (int i = 0; i < t; i++) {
        uint32_t top = 0, bot = 0;
        for (int j = 0; j < t; j++) {
            int a = A[i][j], at = A[j][i];
            int d2 = (i == j) ? D2[i] : 0, dm1 = (i == j) ? Dm1[i] : 0, dm2 = (i == j) ? Dm2[i] : 0;
            int tl, tr, bl, br;
            if (!even) { tl = a ^ d2; tr = d2; bl = d2; br = a ^ dm2; }
            else { tl = d2; tr = a ^ d2; bl = at ^ d2; br = dm1; }
            top |= (uint32_t)tl << j; top |= (uint32_t)tr << (t + j);
            bot |= (uint32_t)bl << j; bot |= (uint32_t)br << (t + j);
        }
        rows[i] = top; rows[t + i] = bot;
    }
    return T2 - rank_rows(rows, T2);
}

static void evaluate(u64 prod) {
    for (int even = 0; even <= 1; even++) {
        u64 k = even ? 2 * prod : prod;
        if (k > N) continue;
        int s = monsky_s(even);
        hist[s]++; total++;
        int need = ((k & 7) == 1 || (k & 7) == 2 || (k & 7) == 3) ? 8 : 7;
        if (s >= need) printf("C %llu %d\n", k, s);
    }
}

static void push(u64 q) {
    for (int i = 0; i < t; i++) {
        int x = jac(q, ps[i]);                                           /* (q / p_i) */
        L[i][t] = (uint8_t)x;
        L[t][i] = (uint8_t)(x ^ (((ps[i] & 3) == 3) && ((q & 3) == 3))); /* (p_i / q), o'zaro qonun */
    }
    Dm1[t] = (q & 3) == 3;
    D2[t] = ((q & 7) == 3) || ((q & 7) == 5);
    Dm2[t] = Dm1[t] ^ D2[t];
    ps[t++] = q;
}

static void dfs(u64 prod, u64 from, int i1, int depth_idx) {
    if (t >= 4) evaluate(prod);
    int need = t >= 3 ? 1 : 4 - t;               /* 4 ta toq tubgacha kamida nechta qolgan */
    int idx = 0;
    for (u64 q = from; q <= M; q += 2) {
        if (!is_prime_odd(q)) continue;
        u128 lb = prod;
        for (int e = 0; e < need; e++) lb *= q;
        if (lb > N) break;
        if (t == 1) {                             /* 2-daraja: shard tanlovi */
            int cur = idx++;
            if ((int)(((u64)i1 * 1000003ULL + (u64)cur) % (u64)NSH) != SH) continue;
        }
        push(q);
        dfs(prod * q, q + 2, t == 1 ? idx : i1, depth_idx + 1);
        t--;
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "foydalanish: %s N [shard nshard]\n", argv[0]); return 1; }
    N = (u64)strtod(argv[1], NULL);
    if (argc >= 4) { SH = atoi(argv[2]); NSH = atoi(argv[3]); }
    M = N / 105 + 2;
    sieve();
    int i1 = 0;
    for (u64 p = 3; p <= M; p += 2) {             /* 1-daraja: birinchi tub */
        if (!is_prime_odd(p)) continue;
        u128 lb = (u128)p * p * p * p;
        if (lb > N) break;
        push(p);
        dfs(p, p + 2, i1, 1);
        t--;
        i1++;
    }
    for (int s = 0; s < 64; s++) if (hist[s]) printf("H %d %llu\n", s, hist[s]);
    printf("T %llu\n", total);
    return 0;
}
