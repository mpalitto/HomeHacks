#!/bin/bash
dir='/home/matteo/dev/node/tensorflow/recordings/'
while true; do
	echo waiting for new intruders...
	dirs="$(ls /home/matteo/dev/node/tensorflow/recordings/new/ 2>/dev/null)"
	if [ "$dirs" ]; then
	   sizeT1=$(du -s $dir/new/ | cut -f1)
	   sizeT0=$sizeT1
	   sizeDiff=$sizeT1
	   while [ $sizeDiff -gt 0 ]
	   do
		   sleep 10; echo waiting for dirs to be complitely written from scanner...
	   	   sizeT1=$(du -s $dir/new/ | cut -f1)
		   sizeDiff=$(($sizeT1 - $sizeT0))
		   sizeT0=$sizeT1
	   done
	   attach="$(ls ${dir}/new/$dirs | sed s_^_\ --attach=${dir}/new/$dirs/_)"
	   if [ $(echo $attach | wc -w) -lt 5 ]; then
		echo 'false detection... NOT sending ALERT email'
	   	mkdir -p ${dir}/old/falseDetections/$dirs
	   	mv ${dir}/new/$dirs/* ${dir}/old/falseDetections/$dirs/
	   	rm -r ${dir}/new/$dirs/
	   else
	   	echo sending files through email...
	   	mail -s "ALLERTA: nuova presenza in casa" $attach daniela.matteo.nicolo@gmail.com <<< "vedi documento allegato :)Matteo"
	   	echo finished sending email
	   	# move the folder with files already sent to the archive "old" folder
	   	# or merge if folder was already in the archive
	   	mkdir -p ${dir}/old/$dirs
	   	mv ${dir}/new/$dirs/* ${dir}/old/$dirs/
	   	rm -r ${dir}/new/$dirs/
	   fi
	fi
	#exit
	sleep 10
done

