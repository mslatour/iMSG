#!/bin/bash

# visualize property/relation distribution
OUTPUT=$(mktemp)

cat debug_relation_stat.txt | sort | uniq -c | sort -rgk 1 | awk '{print $1}' > "${OUTPUT}.relation"
if [ "$(wc -l ${OUTPUT}.relation | awk '{print $1}')" != "1" ]; then
gnuplot -e "set terminal pdf; plot '${OUTPUT}.relation' u 1 w linespoints t 'Relation frequency'" > debug_stat_relation.pdf
gnuplot -e "set terminal pdf; set log xy; plot '${OUTPUT}.relation' u 1 w linespoints t 'Relation log frequency'" > debug_stat_relation_log.pdf
fi

cat debug_property_stat.txt | sort | uniq -c | sort -rgk 1 | awk '{print $1}' > "${OUTPUT}.property"
if [ "$(wc -l ${OUTPUT}.property | awk '{print $1}')" != "1" ]; then
    gnuplot -e "set terminal pdf; plot '${OUTPUT}.property' u 1 w linespoints t 'Property frequency'" > debug_stat_property.pdf
    gnuplot -e "set terminal pdf; set log xy; plot '${OUTPUT}.property' u 1 w linespoints t 'Property log frequency'" > debug_stat_property_log.pdf
fi

# visualize grammar stats
IN="debug_stat.txt"
gnuplot -e "set terminal pdf; plot '$IN' u 1 w linespoints title 'parent parse cost', '$IN' u 2 w linespoints title 'child parse cost', '$IN' u 3 w linespoints title 'child grammar cost', '$IN' u 4 w linespoints title 'parent grammar size', '$IN' u 5 w linespoints title 'child gramar size'" > debug_stat.pdf
