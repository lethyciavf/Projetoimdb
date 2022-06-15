import re
import time
import sqlite3
import pycountry
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from sklearn.feature_extraction.text import CountVectorizer
import warnings
warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")

'''
Perguntas a serem respondidas com esse mini projeto:
1- Quais São as Categorias de Filmes Mais Comuns no IMDB?
2- Qual o Número de Títulos Por Gênero?
3- Qual a Mediana de Avaliação dos Filmes Por Gênero?
4- Qual a Mediana de Avaliação dos Filmes Em Relação ao Ano de Estréia?
5- Qual o Número de Filmes Avaliados Por Gênero Em Relação ao Ano de Estréia?
6- Qual o Filme Com Maior Tempo de Duração? Calcule os Percentis.
7- Qual a Relação Entre Duração e Gênero?
8- Qual o Número de Filmes Produzidos Por País?
9- Quais São os Top 10 Melhores Filmes?
10- Quais São os Top 10 Piores Filmes?
'''

conexao = sqlite3.connect("imdb.db")  #Abre a conexão com o banco de dados

tabelas = pd.read_sql_query("SELECT NAME AS 'Table_Name' FROM sqlite_master WHERE type = 'table'", conexao)

#print(tabelas.head())

tabelas = tabelas["Table_Name"].values.tolist()  #Converte o Table_Name do df em uma lista

'''
#Schemas = coleção de objetos dentro de um db
for tabela in tabelas:
    consulta = "PRAGMA TABLE_INFO ({})".format(tabela)  #PRAGMA tem o mesmo serviço de SELECT mas é exclusivo do sqlite e a sintaxe um pouco diff
    resultado = pd.read_sql_query(consulta, conexao)
    print(f"Esquema da tabela: {tabela}")
    print(resultado)
    print("-" * 100)
'''

#Resposta da primeira pergunta
resultado_1 = pd.read_sql_query("SELECT type, COUNT(*) AS COUNT FROM titles GROUP BY type", conexao)

#Calcula o percentual de cada tipo e coloca o resultado em uma nova coluna chamada percentual - Decisão tomada pelo Analista de Dados
resultado_1["Percentual"] = (resultado_1["COUNT"]/resultado_1["COUNT"].sum()) * 100

''' - Decisão do Analista:
Fazer um gráfico com apenas 4 categorias, sendo 3 primeiras com os titulos mais relevantes e uma ultima chamada de
outros com os demais títulos'''

others = {}  #Criamos em inglês para manter no padrão do db

others["COUNT"] = resultado_1[resultado_1["Percentual"] < 5]["COUNT"].sum()  #Filtra os 5% e soma o total
others["Percentual"] = resultado_1[resultado_1["Percentual"] < 5]["Percentual"].sum()  #Grava o percentual
others["type"] = "others"  #Ajusta o nome

#print(others)


#Modifica o dataframe com os novos parametros
resultado_1 = resultado_1[resultado_1["Percentual"] > 5]  #Filtra resultado_1 só com os valores maiores que 5%
resultado_1 = resultado_1.append(others, ignore_index=True)  #Adiciona a categoria outros ao df inicial
resultado_1 = resultado_1.sort_values(by="COUNT", ascending=False)  #Organiza os valores do maior para o menor


#Configurações do gráfico
f = plt.figure()

cs = cm.Set3(np.arange(100))  #Configuração de cor
plt.pie(resultado_1["COUNT"], labeldistance=1, radius=1.5, colors=cs, wedgeprops=dict(width = 0.5))  #Cria um gráfico de pizza - Rosca, nessa config

#Formatação da legenda
labels = [(f"{str(resultado_1['type'][i])} [{str(round(resultado_1['Percentual'][i], 2))}%]") for i in resultado_1.index]
plt.legend(labels, loc='center', prop={'size': 12})

plt.title("Distribução de Títulos", loc='center', fontdict={'fontsize': 20, 'fontweight': 20})

plt.show()


#