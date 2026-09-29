#!/bin/bash
# a(7) yakuniy quvuri v3: B tugagach bo'shagan yadroda A bo'laklariga TESKARI tartibli qo'shimcha ishchi (mkdir-qulf bilan),
# A + qo'shimcha tugagach A ni qayta yurgizib to'liqlikni tekshiradi, keyin qoldiq → verify_yakun → mwrank.
cd "$(dirname "$0")"
L=yakun.log; A=$1; B=$2; D=$(pwd)
echo "[$(date '+%F %T')] yakun3: B ($B) kutilmoqda" >> $L
while kill -0 "$B" 2>/dev/null; do sleep 60; done
echo "[$(date '+%F %T')] yakun3: B tugadi: $(tail -1 yoqot_B.log) · teskari ishchi boshlandi" >> $L
ls gp_yuqori_A.txt.qismlar/bo_???? | sort -r | xargs -P 1 -n 1 "$D/bo_ishla.sh" &
C=$!
while kill -0 "$A" 2>/dev/null || kill -0 "$C" 2>/dev/null; do sleep 60; done
echo "[$(date '+%F %T')] yakun3: A ($A) va teskari ishchi ($C) tugadi; A qayta tekshiruv" >> $L
./yoqot_gp.sh nomzod_yuqori_A.txt gp_yuqori_A.txt 10 20000 >> $L 2>&1
echo "[$(date '+%F %T')] yakun3: A yakuniy exit=$?" >> $L
cat gp_yuqori_A.txt gp_yuqori_B.txt | sort -n > gp_yuqori.txt
./qoldiq.sh gp_yuqori.txt 3 >> $L 2>&1
cat gp_1e11.txt.qoldiq.natija gp_yuqori.txt.qoldiq.natija > qoldiq_hammasi.txt
python3 verify_yakun.py 797507543734 1e11 natija2_797507543734 natija_1e11 gp_1e11.txt gp_yuqori.txt --qoldiq qoldiq_hammasi.txt > verify_final.txt 2>&1
V=$?
echo "[$(date '+%F %T')] yakun3: verify_yakun exit=$V · $(tail -1 verify_final.txt)" >> $L
../.venv-eclib/bin/python mw_tekshir.py gp_yuqori.txt 1000 10 gp_yuqori.txt.qoldiq.natija > mw_final.txt 2>&1
M=$?
echo "[$(date '+%F %T')] yakun3: mwrank exit=$M · $(tail -1 mw_final.txt)" >> $L
echo "[$(date '+%F %T')] YAKUN3: verify=$V mwrank=$M (0/0 = a(7)=797507543735 isbotlandi)" >> $L
