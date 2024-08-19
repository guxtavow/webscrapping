import subprocess

def Arquivos():
    local = r"C:\Users\e_gustavoaa\OneDrive - SERVICO DE APOIO AS MICRO E PEQUENAS EMPRESAS DE SAO PAULO - SEBRAE\Documentos\projetos\webscrapping\Arquivos"
    # Lista de arquivos a serem executados com seus respectivos diretórios
    arquivos = [
        {'arquivo': 'Atividade_Economica.py', 'diretorio': local},
        {'arquivo': 'CNAE-UF.py', 'diretorio': local},
        {'arquivo': 'Faixa_Etaria.py', 'diretorio': local},
        {'arquivo': 'Municipio.py', 'diretorio': local},
        {'arquivo': 'Municipio2.py', 'diretorio': local}, #ESSE É O MAIS DEMORADO
    ]

    # Loop sobre cada arquivo e executá-lo em um subprocesso no diretório correspondente
    for arquivo_info in arquivos:
        caminho_completo = f'{arquivo_info["diretorio"]}/{arquivo_info["arquivo"]}'
        subprocess.run(['python', caminho_completo])

Arquivos()