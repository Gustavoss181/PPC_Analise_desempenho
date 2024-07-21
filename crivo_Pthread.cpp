/*Código original de Rafael Garcia. 
 * Alterado por Marluce*/
 /*
  * Compilação: g++ -pthread xcrivo.cpp -o xcrivo -fopenmp
  * Execução: ./xcrivo numeroThreads valorN
  * */
#include <iostream>
#include <pthread.h>
#include <cmath>
#include <string>
#include <omp.h>
#include <iomanip>
using namespace std;

long* vet;
long qtd, nt;

void* crivo(void* idt) {
	long id = (long) idt;
	long k;
	
	long start = ceil(((double) id) / nt * (qtd + 1));
	long end = floor(((double) id + 1) / nt * (qtd + 1));

	/* Quando a quantidade de elementos eh multipla da quantidade de threads
	   exige uma correção para evitar a repetição de cálculo entre diferentes
	   threads. Em outras palavras, o ultimo elemento da thread 0 seria tambem
	   calculado pela thread 1 e assim por diante */
	if (qtd % nt == 0) 
		end -= 1;
	
	/* Excluindo os elementos 0 E 1, apenas no caso da primeira thread */
	if (start == 0) 
		k = 2;
	
	else 
		k = start;
	
	/* Caso o final seja igual ao tamanho do vetor, subtrai-se 1, uma vez que
	   o vetor de tamanho N tem posicoes de 0 a N - 1*/
	if (end == qtd + 1)
		end -= 1;

	/* Alem da condicao do algoritmo do crivo, checar se o k tem, no maximo,
	   o valor END, para uma thread nao executar a funcao de outra thread*/
	while ((k * k <= qtd) and (k <= end)){
		for (int c = k * k; c <= qtd; c = c + k) vet[c] = -1;
		
		k++;
		
							    // Verificacao do k em cada incremento
		while ((vet[k] == -1) and (k <= end)){
		  k++;
		}
	}
	return NULL;
}

int main(int argc, char* argv[]) {
	nt =  stoi(argv[1]); //definindo número de threads
	
	qtd = stoi(argv[2]); //qtd de num no intervalo
	
	long v[qtd + 1];
	
	for (long c = 0; c <= qtd; c++) {
		v[c] = c;
	}
	
	vet = v;
	/*
	for (int c = 0; c <= qtd; c++) {
		cout << vet[c] << " ";
	}
	
	cout << endl;
	* */
	double time1 = omp_get_wtime();
	
	pthread_t id[nt]; //vetor de threads
	
	//loop para criacao de threads
	for (long c = 0; c < nt; c++) {
		id[c] = c;
		pthread_create(&id[c], NULL, crivo, (void*) id[c]);
	}
	
	//usando join para esperar o resultado
	for (long c = 0; c < nt; c++) {
		pthread_join(id[c], NULL);
	}
	
	
	//imprimindo
	
	
	for (int c = 2; c <= qtd; c++) {
		if (vet[c] != -1) {
			//cout << vet[c] << " ";
		}
	}
	//cout << "Tempo paralelo: ";
	cout << setprecision(6) << fixed << omp_get_wtime() - time1;
	/*
	cout << endl << "Não primos:" << endl;
	
	for (int c = 0; c <= qtd; c++) {
		if (vet[c] == -1) {
			cout << c << " ";
		}
	}
	cout << endl;*/
}
