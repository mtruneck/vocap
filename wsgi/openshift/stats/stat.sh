#!/bin/bash

C=0; 
I=0
for TERM in `echo $(cat terms.txt)`; do 
	if echo $TERM | aspell -a | grep -q '*'; then 
		C=`expr $C + 1`
	fi
	I=`expr $I + 1`
	if [ `expr $I % 500` -eq 3 ]; then echo -n "."; fi
done

echo $C

