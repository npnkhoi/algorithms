# $1: the source image
# $2: the destination image
# loop through k in [2, 5, 10, 15, 20]

for k in 2 5 10 15 20
do
    python kmeans.py $1 $k $2-$k.jpg
    # show the size of the image
    du -h $2-$k.jpg
done