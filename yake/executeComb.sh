#for d in `ls ../Datasets/`; do
#	echo $d;
#	python3 clientyake.py -i ../Datasets/$d/docsutf8/ -n 2 -ws 2 -df leve -dl 1.00 -t 50 > /dev/null &
#done;
#wait;


#for ws in 1 2 3 4 6 8; do
#	for n in 1 2 3 4; do
#		python3 clientyake.py -i ../Datasets/{kdd,www,WKC}/docsutf8/ -n $n -ws $ws -df leve -dl 1.00 -t 50 > /dev/null &
#	done
#	python3 clientyake.py -i ../Datasets/{kdd,www,WKC}/docsutf8/ -n 5 -ws $ws -df leve -dl 1.00 -t 50
#done

# Features KPF WCase WFreq WPos WRel WSpread

python3 clientyake.py -i ../Datasets/kdd/docsutf8/ ../Datasets/www/docsutf8/ ../Datasets/WKC/docsutf8/ -n 2 -ws 1 -df leve -dl 1.00 -f WCase WFreq WPos WRel WSpread -t 50 > /dev/null &
python3 clientyake.py -i ../Datasets/kdd/docsutf8/ ../Datasets/www/docsutf8/ ../Datasets/WKC/docsutf8/ -n 2 -ws 1 -df leve -dl 1.00 -f KPF WFreq WPos WRel WSpread -t 50 > /dev/null &
python3 clientyake.py -i ../Datasets/kdd/docsutf8/ ../Datasets/www/docsutf8/ ../Datasets/WKC/docsutf8/ -n 2 -ws 1 -df leve -dl 1.00 -f KPF WCase WPos WRel WSpread -t 50 > /dev/null &
python3 clientyake.py -i ../Datasets/kdd/docsutf8/ ../Datasets/www/docsutf8/ ../Datasets/WKC/docsutf8/ -n 2 -ws 1 -df leve -dl 1.00 -f KPF WCase WFreq WRel WSpread -t 50 > /dev/null &
python3 clientyake.py -i ../Datasets/kdd/docsutf8/ ../Datasets/www/docsutf8/ ../Datasets/WKC/docsutf8/ -n 2 -ws 1 -df leve -dl 1.00 -f KPF WCase WFreq WPos WSpread -t 50 > /dev/null &
python3 clientyake.py -i ../Datasets/kdd/docsutf8/ ../Datasets/www/docsutf8/ ../Datasets/WKC/docsutf8/ -n 2 -ws 1 -df leve -dl 1.00 -f KPF WCase WFreq WPos WRel -t 50

for dF in seqm; do
	for dL in `seq 0.1 0.1 1. | tr , .`; do
		for w in 1 2 3 4 6 8 10; do
			python3 clientyake.py -i ../Datasets/kdd/docsutf8/ ../Datasets/www/docsutf8/ ../Datasets/WKC/docsutf8/ -n 2 -ws $w -df seqm -dl $dL -t 50 > /dev/null &
       		done
		echo $dF $dL
		wait
	done
done


for dF in leve jaro seqm; do
        for dL in `seq 0.1 0.1 1. | tr , .`; do
                for n in 1 2 3 4 5; do
                        python3 clientyake.py -i ../Datasets/kdd/docsutf8/ ../Datasets/www/docsutf8/ ../Datasets/WKC/docsutf8/ -n $n -ws 1 -df $dF -dl $dL -t 50 > /dev/null &
                done
                echo $dF $dL
                wait
        done
done
