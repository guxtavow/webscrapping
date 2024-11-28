# WEBSCRAPPING - MEI's

Este script tem como finalidade retornar as informações do site do MEI(Receita), além de salvar as informações e criar as pastas por ano e mês na rede da UGE - SEBRAE SP.

---

## FUNCIONALIDADES
- Mapeia diversas informações do site;
- Retorna informações sobre Município, Atividades Economicas, Genero, CNAE e Faixa Etaria sobre os MEI's de São Paulo;
- Salva automaticamente os arquivos em pastas especificas, baseada no ano atual e o mês anterior;
- Em alguns script, retorna informação sobre todos os municípios de São Paulo.

## REQUISITOS
Certifique-se de ter o **Python(v3.8+)** instalado, logo depois instale também as bibliotecas necessárias dentro do arquivo `requirements.txt`, para executar essa ação, coloque no terminal o seguinte código:
```bash
pip install -r requirements.txt
```

## ESTRUTURAÇÃO DO PROJETO
- Webscrapping - MEI
    * Arquivos
        * **Atividade_Economica.py**    #Traz as informações dos MEIS de Atividade Economica
        * **CNAE-UF.py**     #Traz as informações dos MEIS de CNAE por UF
        * **Faixa_Etaria.py**   #Traz as informações dos MEIS de Faixa Etaria
        * **Municipio.py**       #Traz as informações dos MEIS por Municipio
        * **Municipio2.py**      #Traz as informações dos MEIS por Municipio e Genero, passando por TODOS os municipios de São Paulo
        * **municipios.json**   #Mapeia todos os ID's dos municipios para caso haja alguma quebra na execução do codigo, ele saber o id do municipio que deu erro e continuar a partir dele
    * **Exec.py**   # Executa todos os scripts da pasta 'Arquivos', em ordem

## COMO EXECUTAR
Para executar esse scripts é bem simples, rode apenas o arquivo `Exec.py` pois assim, ele rodará todos os outros scripts. Agora se quiser apenas uma informação específica, rode o script do dado que você deseja. 

**Lembrando que:**
Sempre que você rodar esse arquivo, será criada uma pasta na rede da UGE com o ano e o mês passado (partindo do mês que você esta)que esse script foi executado, por isso, é recomendável executar este script apenas no começo de cada mês.


## COMO FUNCIONA
O script entra no site do MEI, identifica todos os links da pagina inicial, clicando em cada um que é necessário obter a informação e fazendo todo o processo de identificar as variaveis necessárias para exportar o xlsx com os dados do MEI.

Logo após isso, ele mapeia nossa rede da UGE, obtem o mês e o ano atual e retorna o ano + o mês anterior como nome de uma nova pasta que será criada em um diretório especifico para cada dado, afinal os resultados no site do MEI, são "fotografias" acumuladas de dados, que são atualizadas a cada semana.

**Obs:** O script `Municipio2.py` é o mais demorado dentre os códigos, pois ele passa por todos os Municípios de São Paulo. Por conta disso, caso haja algum erro no meio da execução do codigo, é só rodar novamente, pois ele passa por todos os ids e os nomes dos arquivos já gerados e continua a partir da onde deu o erro.

## DIRETORIOS

UGE > Pesquisas > Econômicas > MEI_Estatísticas

Caminho: Z:\Pesquisas\Econômicas\MEI_Estatísticas

a) Atividade Econômica > Brasil 
b) CNAE/UF > Estado de São Paulo 
c) CNAE/Município > Municípios de São Paulo 
d) CNAE UF/Município/Sexo > Estado de São Paulo por Sexo