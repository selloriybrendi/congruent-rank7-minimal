#!/bin/bash
# r2 >= 7 qolgan nomzodlar uchun ikki bosqich:
#  (1) izogeniya sinfi: rang izogeniyada o'zgarmaydi → sinfdagi har egri chiziqda ellrank, eng kichik r2 = shartsiz yuqori chegara;
#  (2) effort oshirib nuqta qidirish (r1). r1 = 7 → k < 797507543735 da rang 7 (a(7) pastga tushadi); r1 < 7 <= r2min → ochiq teshik.
# foydalanish: ./qoldiq.sh gp_natija.txt [effort=3]  → "$IN.qoldiq.natija": "k r1max r2min"
IN=$1; EF=${2:-3}
awk '$3!="ERR" && $3>=7 {print $1}' "$IN" > "$IN.qoldiq"
echo "qoldiq nomzodlar: $(wc -l < "$IN.qoldiq")"
: > "$IN.qoldiq.natija"
[ -s "$IN.qoldiq" ] || exit 0
gp -q -s 2000000000 2>&1 > "$IN.qoldiq.natija" <<GP
default(nbthreads, 1); v = readvec("$IN.qoldiq");
for(i = 1, #v, L = ellisomat(ellinit([0,0,0,-v[i]^2,0]))[1]; r1 = 0; r2 = 99; for(j = 1, #L, c = L[j]; if(type(c[1]) == "t_VEC", c = c[1]); r = ellrank(ellinit(c), $EF); r1 = max(r1, r[1]); r2 = min(r2, r[2])); print(v[i], " ", r1, " ", r2)); quit
GP
cat "$IN.qoldiq.natija"
echo "izogeniya bilan ham r2>=7 qolganlar: $(awk '$3>=7' "$IN.qoldiq.natija" | wc -l)"
