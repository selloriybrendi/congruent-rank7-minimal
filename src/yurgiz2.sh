#!/bin/bash
# foydalanish: ./yurgiz2.sh N [NSH=40] [P=10]  → NSH shard, bir vaqtda P jarayon (xargs), natija: natija2_N/
N=$1; NSH=${2:-40}; P=${3:-10}; D=natija2_$N; mkdir -p $D
seq 0 $((NSH-1)) | xargs -P $P -I{} sh -c "[ -f $D/shard_{}.done ] || (./monsky_elak $N {} $NSH > $D/shard_{}.txt && touch $D/shard_{}.done)"
ls $D/shard_*.done | wc -l | xargs -I{} echo "tugagan shard: {} / $NSH"
cat $D/shard_*.txt | awk '/^H/{h[$2]+=$3} /^T/{t+=$2} END{for(s in h) printf "H %s %d\n", s, h[s]; printf "T %d\n", t}' | sort -k2 -n > $D/jami.txt
grep -h '^C' $D/shard_*.txt | awk '{print $2, $3}' | sort -n > $D/nomzod.txt
echo "N=$N: $(grep ^T $D/jami.txt) · nomzod: $(wc -l < $D/nomzod.txt)"
