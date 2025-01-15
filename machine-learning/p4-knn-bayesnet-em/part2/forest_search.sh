for k in 2 5 10 20 
do
	for r in 0.1 0.2 0.5 
	do
		echo ===== k=$k r=$r =====
		python train.py forest -n $k -s 1 -hr $r -e valid
	done
done

