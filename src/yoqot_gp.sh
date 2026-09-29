#!/bin/bash
# yoqot_gp v2 — davom ettiriladigan, jim yutishsiz yo'qqa chiqarish.
# PARI mt deadlock (gen_inccrt -> mt_queue_reset -> _pthread_join) sabab nbthreads=1 majburiy.
# foydalanish: ./yoqot_gp2.sh nomzod.txt natija.txt [P=10] [BO'LAK=20000]
#   har qator: "k r1 r2" (r2 < 7 => yo'qqa chiqdi); ellrank xatosi → "k ERR ERR" (yo'qqa chiqmagan deb sanaladi)
#   oxirida: nomzodlar to'plami = natijalar to'plami tekshiriladi; mos kelmasa exit 3.
IN=$1; OUT=$2; P=${3:-10}; B=${4:-20000}; T="$OUT.qismlar"
SHA=$(shasum -a 256 "$IN" | cut -c1-64)
if [ ! -f "$T/INPUT.sha" ] || [ "$(cat "$T/INPUT.sha")" != "$SHA" ]; then
  rm -rf "$T"; mkdir -p "$T"
  awk '{print $1}' "$IN" | split -l "$B" -a 4 - "$T/bo_"
  echo "$SHA" > "$T/INPUT.sha"
fi
# v3: o'lik qulflarni tozalash (faqat yakka orkestrator chaqirganda xavfsiz)
for L in "$T"/bo_????.lock; do [ -d "$L" ] || continue; p=$(cat "$L/pid" 2>/dev/null); kill -0 "$p" 2>/dev/null || rm -rf "$L"; done
ls "$T"/bo_???? | xargs -P "$P" -n 1 "$(cd "$(dirname "$0")" && pwd)/bo_ishla.sh"
cat "$T"/bo_????.out | sort -n > "$OUT"
NIN=$(wc -l < "$IN"); NOUT=$(wc -l < "$OUT"); NDONE=$(ls "$T"/bo_????.done 2>/dev/null | wc -l); NB=$(ls "$T"/bo_???? | wc -l)
FARQ=$(comm -3 <(awk '{print $1}' "$IN" | sort) <(awk '{print $1}' "$OUT" | sort) | wc -l)
echo "$NOUT / $NIN natija · bo'lak $NDONE / $NB · to'plam farqi: $FARQ · ERR: $(grep -c ERR "$OUT") · r2>=7 (QOLDI): $(awk '$3!="ERR" && $3>=7' "$OUT" | wc -l) · r2 taqsimoti: $(awk '{print $3}' "$OUT" | sort -n | uniq -c | tr '\n' ' ')"
[ "$FARQ" -eq 0 ] && [ "$NDONE" -eq "$NB" ] || { echo "XATO: to'liqlik buzilgan"; exit 3; }
[ "$(grep -c ERR "$OUT")" -eq 0 ] || { echo "OGOH: ellrank xatosi bor (ERR qatorlar yo'qqa chiqmagan)"; exit 4; }
