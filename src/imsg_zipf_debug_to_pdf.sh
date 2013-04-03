#!/bin/bash

OUTPUT=$(mktemp)
cat debug_relation_zipf.txt | sort | uniq -c | sort -rgk 1 | awk '{print $1}' > "${OUTPUT}.relation"
cat debug_property_zipf.txt | sort | uniq -c | sort -rgk 1 | awk '{print $1}' > "${OUTPUT}.property"
paste -d" " "${OUTPUT}.relation" "${OUTPUT}.property" > "${OUTPUT}.both"
gnuplot -e "set terminal pdf; plot '${OUTPUT}.both' u 1 w linespoints title 'relation', '${OUTPUT}.both' u 2 w linespoints title 'property'" > debug_zipf.pdf
