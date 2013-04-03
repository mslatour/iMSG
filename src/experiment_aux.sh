#!/bin/bash

# Options from command line
i="$1"
I="$2"
e="$3"
s="$4"
if [ "$5" == "1" ]; then m="-m"; else m=""; fi
if [ "$6" == "1" ]; then t="-t"; else t=""; fi

# format options for filename
estring=$(echo "$e" | sed 's/\.//g')
if [ -z "$m" ]; then mstring="F"; else mstring="T"; fi
if [ -z "$t" ]; then tstring="F"; else tstring="T"; fi

echo "Running: python world.py -i $i -I $I -e $e -s $s -d $m $t"
python world.py -i $i -I $I -e $e -s $s -d $m $t
./imsg_stat_to_pdf.sh
if [ -e "debug_stat.pdf" ]; then
    mv "debug_stat.pdf" "debug_${i}_${I}_${estring}_${s}_${mstring}_${tstring}_stat.pdf"
fi
if [ -e "debug_stat_relation.pdf" ]; then
    mv "debug_stat_relation.pdf" "debug_${i}_${I}_${estring}_${s}_${mstring}_${tstring}_stat_relation.pdf"
fi
if [ -e "debug_stat_relation_log.pdf" ]; then
    mv "debug_stat_relation_log.pdf" "debug_${i}_${I}_${estring}_${s}_${mstring}_${tstring}_stat_relation_log.pdf"
fi
if [ -e "debug_stat_property.pdf" ]; then
    mv "debug_stat_property.pdf" "debug_${i}_${I}_${estring}_${s}_${mstring}_${tstring}_stat_property.pdf"
fi
if [ -e "debug_stat_property_log.pdf" ]; then
    mv "debug_stat_property_log.pdf" "debug_${i}_${I}_${estring}_${s}_${mstring}_${tstring}_stat_property_log.pdf"
fi
