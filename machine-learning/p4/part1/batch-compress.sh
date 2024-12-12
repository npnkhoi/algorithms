# $1: the source image
# $2: the destination image
# loop through k in [2, 5, 10, 15, 20]

for k in 2 5 10 15 20
do
    for samp in 1 2 3 4 5
    do
    	python kmeans.py $1 $k $2-$k-$samp.jpg
    	# show the size of the image
    	du -h $2-$k-$samp.jpg
    done
done
