import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore

def plotar_grafico_barras(df, coluna, titulo, ylabel):
    # Prepara dados para o gráfico
    n_values = df['N'].unique()
    num_threads = df['NumThreads'].unique()

    # Configurações para o gráfico
    bar_width = 0.1
    x = np.arange(len(n_values))  # as posições dos grupos de N

    # Cria a figura e o eixo
    fig, ax = plt.subplots(figsize=(14, 8))

    # Adiciona barras para cada número de threads
    for i, nThreads in enumerate(num_threads):
        # Filtra os dados para o valor específico de NumThreads
        subset = df[df['NumThreads'] == nThreads]
        
        # Posição da barra
        offset = bar_width * i
        
        # Adiciona as barras
        rects = ax.bar(x + offset, subset[coluna], bar_width, label=f'Threads={nThreads}')
        # ax.bar_label(rects, padding=3)

    # Configura o gráfico
    ax.set_xlabel('Valores de N')
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    ax.set_xticks(x + bar_width * (len(num_threads) - 1) / 2)
    ax.set_xticklabels(n_values)
    ax.legend(title='Número de Threads')

    # Exibe o gráfico
    plt.tight_layout()
    # plt.show()

def plotar_grafico_linhas(df, coluna, titulo, ylabel):
    # Prepara dados para o gráfico
    n_values = df['N'].unique()
    num_threads = df['NumThreads'].unique()

    # Configurações para o gráfico
    x = np.arange(len(n_values))  # as posições dos grupos de N

    # Cria a figura e o eixo
    fig, ax = plt.subplots(figsize=(14, 8))

    # Adiciona barras para cada número de threads
    for nThreads in num_threads:
        # Filtra os dados para o valor específico de NumThreads
        if nThreads != 1:
            subset = df[df['NumThreads'] == nThreads]
            ax.plot(x, subset[coluna], marker='o', label=f'Threads={nThreads}')
            ax.set_label(subset[coluna])
            # ax.bar_label(rects, padding=3)

    # Configura o gráfico
    ax.set_xlabel('Valores de N')
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    ax.set_xticks(x)
    ax.set_xticklabels(n_values)
    ax.legend(title='Número de Threads')

    # Exibe o gráfico
    plt.tight_layout()
    # plt.show()

def plotar_tabela(df):
    # Cria a figura e o eixo
    fig, ax = plt.subplots(figsize=(14, 8)) # Ajusta o tamanho da figura conforme necessário

    # Oculta o eixo
    ax.axis('off')
    ax.axis('tight')

    # Adiciona a tabela ao gráfico
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    # Ajusta o layout para garantir que a tabela se encaixe na figura
    fig.tight_layout()

    # Exibe o gráfico com a tabela
    # plt.show()

def format_number(num):
    if isinstance(num, (int, float)):
        return f'{num:.4f}' if num % 1 != 0 else f'{int(num)}'
    return num

# Leitura do arquivo CSV
df = pd.read_csv('dados-omp.csv', sep='\s', engine='python')

# Calcula a média dos tempos
df['Media'] = df[['tempo1', 'tempo2', 'tempo3']].mean(axis=1)

# Exibe as primeiras linhas do dataframe para verificar se a leitura e o cálculo foram corretos
print(df.head())
plotar_grafico_barras(df, 'Media', 'Média dos Tempos por Número de Threads e Valor de N', 'Média dos Tempos (segundos)')

# Calcula o speedup
tempo_sequencial = df[df['NumThreads'] == 1][['N', 'Media']].rename(columns={'Media': 'TempoSequencial'})
df = df.merge(tempo_sequencial, on='N')
df['Speedup'] = df['TempoSequencial'] / df['Media']
plotar_grafico_linhas(df, 'Speedup', 'Speedup dos Tempos por Número de Threads e Valor de N', 'Speedup')

# Calcula a eficiência
df['Eficiencia'] = df['Speedup']/df['NumThreads']
plotar_grafico_linhas(df, 'Eficiencia', 'Eficiencia por numero de threads', 'Eficiência')

# Calcula a métrica de Karp-Flat
df['MetricaKarpFlat'] = ((1/df['Speedup']) - (1/df['NumThreads']))/(1 - (1/df['NumThreads']))
KarpFlat_df = df[df['NumThreads'] != 1][['N', 'NumThreads', 'MetricaKarpFlat']].map(format_number)
plotar_tabela(KarpFlat_df)

# print(df.head())

plt.show()