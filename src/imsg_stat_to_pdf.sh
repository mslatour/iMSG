#!/bin/bash

# visualize property/relation distribution
OUTPUT=$(mktemp)
cat debug_relation_stat.txt | sort | uniq -c | sort -rgk 1 | awk '{print $1}' > "${OUTPUT}.relation"
cat debug_property_stat.txt | sort | uniq -c | sort -rgk 1 | awk '{print $1}' > "${OUTPUT}.property"
paste -d" " "${OUTPUT}.relation" "${OUTPUT}.property" > "${OUTPUT}.both"
gnuplot -e "set terminal pdf; plot '${OUTPUT}.both' u 1 w linespoints title 'relation', '${OUTPUT}.both' u 2 w linespoints title 'property'" > debug_stat_property_relation.pdf

# visualize grammar stats
IN="debug_stat.txt"
gnuplot -e "set terminal pdf; plot '$IN' u 1 w linespoints title 'parent parse cost', '$IN' u 2 w linespoints title 'child parse cost', '$IN' u 3 w linespoints title 'child grammar cost', '$IN' u 4 w linespoints title 'parent grammar size', '$IN' u 5 w linespoints title 'child gramar size'" > debug_stat.pdf
