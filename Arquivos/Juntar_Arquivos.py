import os
import pandas as pd
 
# Defina o caminho para a pasta contendo os arquivos CSV
caminho_pasta = r'C:\Users\e_gustavoaa\OneDrive - SERVICO DE APOIO AS MICRO E PEQUENAS EMPRESAS DE SAO PAULO - SEBRAE\Documentos\projetos\24-07'
 
# Crie uma lista para armazenar os DataFrames temporários
dataframes = []
 
# Percorra todos os arquivos na pasta
for arquivo in os.listdir(caminho_pasta):
    if arquivo.endswith('.csv'):
        # Obtenha o caminho completo do arquivo
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        # Leia o arquivo CSV usando o caminho correto
        df_temp = pd.read_csv(caminho_arquivo, encoding='ISO-8859-1')
        # Extraia o nome do município (removendo a extensão .csv)
        municipio = os.path.splitext(arquivo)[0]
        # Adicione a coluna 'municipio' ao DataFrame
        df_temp['municipio'] = municipio
        # Adicione o DataFrame à lista
        dataframes.append(df_temp)
 
# Concatene todos os DataFrames em um único DataFrame final
df_final = pd.concat(dataframes, ignore_index=True)
print(df_final.size)
print(df_final.head())
df_final.to_csv('teste.csv',index=False)
# Agora df_final contém todos os dados com a coluna 'municipio'