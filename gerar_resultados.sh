#!/bin/sh
saida_omp="dados-omp.csv"
if [ -f $saida_omp ]; then
	rm $saida_omp
fi
gcc -fopenmp crivo-openmp.c -lm -o crivo-openmp.o

# Cabeçalho
echo 'N NumThreads tempo1 tempo2 tempo3' >> $saida_omp
# Conteúdo
for N in 1000 10000 100000 1000000; do
	./crivo-openmp.o $N t 8 3 >> $saida_omp
done
echo '\n' >> $saida_omp


saida_pthread="dados-pthread.csv"
if [ -f $saida_pthread ]; then
	rm $saida_pthread
fi
g++ -pthread -fopenmp crivo_Pthread.cpp -o crivo_Pthread.o

# Cabeçalho
echo 'N NumThreads tempo1 tempo2 tempo3' >> $saida_pthread
# Conteúdo
for n in 1000 10000 100000 1000000; do
	for nthreads in 1 2 3 4 5 6 7 8; do
        echo -n $n $nthreads '' >> $saida_pthread
        for i in 1 2 3; do
            ./crivo_Pthread.o $nthreads $n >> $saida_pthread
            echo -n ' ' >> $saida_pthread
        done
		echo '' >> $saida_pthread
	done
done

cat analise_e_conclusao.txt
