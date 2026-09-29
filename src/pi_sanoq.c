/* pi_sanoq.c — elak to'liqligining MUSTAQIL tekshiruvi.
 * monsky_elak har bir k ni alohida sanaydi (T); bu yerda esa oxirgi tub bo'luvchi π(x) jadvalidan sanaladi:
 *   F(x) = #{toq kvadratsiz k <= x, tub bo'luvchilar soni >= 4},   T(N) = F(N) + F(N/2).
 * Har tugun (t >= 3 tub tanlangan, ko'paytma prod, oxirgi tub p) bolalari soni = π_toq(x/prod) − π_toq(p).
 * Foydalanish: ./pi_sanoq N   → "T <son>"  (monsky_elak ning "T" qatori bilan teng bo'lishi shart) */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef unsigned long long u64;
typedef unsigned __int128 u128;

static u64 M;              /* jadval chegarasi */
static uint64_t *bits;     /* toq x uchun: bit (x-1)/2 = 1 agar x tub */
static uint32_t *pre;      /* pre[w] = 0..w-1 so'zlardagi tublar soni */
static u64 *P, np;         /* toq tublar ro'yxati (DFS uchun, <= M) */

static void build(u64 pmax) {
    u64 nb = (M >> 1) + 1, nw = (nb >> 6) + 1;          /* bit i: 2i+1 */
    bits = calloc(nw, 8); pre = calloc(nw + 1, 4);
    if (!bits || !pre) { fprintf(stderr, "xotira\n"); exit(1); }
    bits[0] |= 1ULL;                                     /* 1 tub emas */
    for (u64 p = 3; p * p <= M; p += 2)                  /* murakkablarni belgilash */
        if (!(bits[(p >> 1) >> 6] >> ((p >> 1) & 63) & 1))
            for (u64 q = p * p; q <= M; q += 2 * p) bits[(q >> 1) >> 6] |= 1ULL << ((q >> 1) & 63);
    for (u64 w = 0; w < nw; w++) bits[w] = ~bits[w];     /* endi 1 = tub */
    u64 last = nb & 63;                                  /* jadvaldan tashqaridagi bitlarni o'chirish */
    if (last) bits[nb >> 6] &= (1ULL << last) - 1; else bits[nb >> 6] = 0;
    for (u64 w = (nb >> 6) + 1; w < nw; w++) bits[w] = 0;
    for (u64 w = 0; w < nw; w++) pre[w + 1] = pre[w] + (uint32_t)__builtin_popcountll(bits[w]);
    P = malloc((pmax / 2 + 2) * 8); np = 0;              /* DFS uchun kichik tublar ro'yxati */
    for (u64 x = 3; x <= pmax && x <= M; x += 2)
        if (bits[(x >> 1) >> 6] >> ((x >> 1) & 63) & 1) P[np++] = x;
}

/* toq tublar soni <= x (x <= M) */
static inline u64 pi_odd(u64 x) {
    if (x < 3) return 0;
    u64 i = (x - 1) >> 1, w = i >> 6;
    uint64_t m = (i & 63) == 63 ? ~0ULL : ((1ULL << ((i & 63) + 1)) - 1);
    return pre[w] + (u64)__builtin_popcountll(bits[w] & m);
}

static u64 X;

static int oshdi = 0;   /* DFS tublar ro'yxati tugab qolsa — natija ishonchsiz */

/* tugun: prod, t tub, oxirgi tub pl, keyingi tub indeksi j (P[j] > pl) */
static u64 g(u64 prod, int t, u64 pl, u64 j) {
    u64 s = 0, lim = X / prod;
    if (t >= 3 && lim > pl) s += pi_odd(lim) - pi_odd(pl);   /* bolalar: t+1 >= 4 */
    int need = t >= 3 ? 2 : 4 - t;                           /* bolaning o'zi yana tugun bo'lishi uchun */
    u64 i = j;
    for (; i < np; i++) {
        u64 q = P[i];
        u128 lb = prod;
        for (int e = 0; e < need; e++) lb *= q;
        if (lb > X) break;
        s += g(prod * q, t + 1, q, i + 1);
    }
    if (i == np) oshdi = 1;
    return s;
}

static u64 F(u64 x) { X = x; return g(1, 0, 1, 0); }

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "foydalanish: %s N\n", argv[0]); return 1; }
    u64 N = (u64)strtod(argv[1], NULL);
    M = N / 105 + 2;
    u64 pmax = 3;
    while ((u128)pmax * pmax * 15 <= N) pmax++;
    build(pmax + 1000);
    u64 a = F(N), b = F(N / 2);
    if (oshdi) { fprintf(stderr, "XATO: DFS tublar ro'yxati yetmadi\n"); return 2; }
    printf("F(N) %llu\nF(N/2) %llu\nT %llu\n", a, b, a + b);
    return 0;
}
