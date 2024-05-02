import subprocess

def Arquivos():
    # Lista de arquivos a serem executados com seus respectivos diretórios
    arquivos = [
        {'arquivo': 'Atividade_Economica.py', 'diretorio': r'C:\Users\e_gustavoaa\Documents\projetos\webscrapping\Atividade Economica'},
        {'arquivo': 'CNAE-UF.py', 'diretorio': r'C:\Users\e_gustavoaa\Documents\projetos\webscrapping\CNAE-UF'},
        {'arquivo': 'Municipio.py', 'diretorio': r'C:\Users\e_gustavoaa\Documents\projetos\webscrapping\Municipio'},
        {'arquivo': 'Municipio2.py', 'diretorio': r'C:\Users\e_gustavoaa\Documents\projetos\webscrapping\Municipio2'}
    ]

    # Loop sobre cada arquivo e executá-lo em um subprocesso no diretório correspondente
    for arquivo_info in arquivos:
        caminho_completo = f'{arquivo_info["diretorio"]}/{arquivo_info["arquivo"]}'
        subprocess.run(['python', caminho_completo])

Arquivos()