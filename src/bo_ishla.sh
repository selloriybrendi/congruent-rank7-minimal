#!/bin/bash
# bitta bo'lakni yo'qqa chiqarish (yoqot_gp.sh chaqiradi): $1 = bo'lak fayli (har qatorda faqat k)
# v3 (2026-09-28 13:30): egri chiziq E_k o'rniga 2-izogen y^2=x^3+4k^2x — rang izogeniyada o'zgarmaydi, r2 shartsiz; 1.80x tez (500 namuna). A5 nazorat: a(5),a(6),a(7) → r2 5,6,7.
# v2: mkdir-qulf — bir bo'lakni ikki ishchi bir vaqtda hisoblamaydi (teskari tartibli qo'shimcha ishchi uchun).
#     O'lik qulflar faqat yakka ishchi paytida (yoqot_gp.sh boshida) tozalanadi — parallel paytda qulf olib qo'yilmaydi.
f=$1
[ -f "$f.done" ] && exit 0
mkdir "$f.lock" 2>/dev/null || exit 0
echo $$ > "$f.lock/pid"
[ -n "$BO_LOG" ] && echo "$f $$" >> "$BO_LOG"
gp -q -s 2000000000 > "$f.out" 2> "$f.err" <<GP
default(nbthreads, 1); v = readvec("$f"); for(i = 1, #v, r = iferr(ellrank(ellinit([0,0,0,4*v[i]^2,0])), e, "ERR"); if(type(r) == "t_VEC", print(v[i], " ", r[1], " ", r[2]), print(v[i], " ERR ERR"))); quit
GP
[ "$(wc -l < "$f.out")" -eq "$(wc -l < "$f")" ] && { touch "$f.done"; echo izogen > "$f.usul"; }
rm -rf "$f.lock"
