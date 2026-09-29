#!/bin/bash
# foydalanish: ./yurgiz.sh N   → 10 shard parallel, natija: natija_N/shard_*.txt + jamlanma
N=$1; D=natija_$N; mkdir -p $D
for i in $(seq 0 9); do ./monsky_elak $N $i 10 > $D/shard_$i.txt & done; wait
cat $D/shard_*.txt | awk '/^H/{h[$2]+=$3} /^T/{t+=$2} /^C/{print $2, $3 > "'$D'/nomzod.txt"} END{for(s in h) printf "H %s %d\n", s, h[s]; printf "T %d\n", t}' | sort -k2 -n > $D/jami.txt
sort -n -o $D/nomzod.txt $D/nomzod.txt 2>/dev/null; touch $D/nomzod.txt
echo "N=$N: $(grep ^T $D/jami.txt) · nomzod: $(wc -l < $D/nomzod.txt)"
