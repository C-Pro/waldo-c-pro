#!/bin/bash
for f in *.jpg
do
	convert "$f" -crop 100x100+1000+1000 "crop_$f"
done

