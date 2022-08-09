#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Bibliotecas usadas

# Web Scraping
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Extração de dados via API
import requests
import json

# Tratamento dos dados
import pandas as pd
import re

# Conexão com banco de dados
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


# # Definindo Algumas Funções

# ## Função para capturar o código html de um site

# In[7]:


def captura_html(URL):
    HEADERS = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    try:
        REQUEST = Request(URL, headers = HEADERS)
        HTML = urlopen(REQUEST).read()
        return HTML

    except HTTPError as e:
        print(e.status, e.reason)

    except URLError as e:
        print(e.reason)


# ## Função que traduz os tipos dos pokemons

# In[8]:


def traduz_tipo(tipo):
    
    # Criando dicionário com os tipos traduzidos
    tradutor = {
        'Normal' : 'Normal',
        'Fire' : 'Fogo',
        'Water' : 'Água',
        'Grass' : 'Planta',
        'Flying' : 'Voador',
        'Fighting' : 'Lutador',
        'Poison' : 'Veneno',
        'Electric' : 'Elétrico',
        'Ground' : 'Solo',
        'Rock' : 'Pedra',
        'Psychic' : 'Psíquico',
        'Ice' : 'Gelo',
        'Bug' : 'Inseto',
        'Ghost' : 'Fantasma',
        'Steel' : 'Metal',
        'Dragon' : 'Dragão',
        'Dark' : 'Noturno',
        'Fairy' : 'Fada'
    }

    # Comparando a input da função com os pares e substituindo
    pares = list(tradutor.items())
    for i in range(len(pares)):
        if pares[i][0] in tipo:
            tipo = tipo.replace(pares[i][0], pares[i][1])
    
    return tipo


# ## Função que sobe dataframe para o banco de dados

# In[9]:


def envia_postgres(DATAFRAME, ENGINE, NOME_TABELA):
    try:
        DATAFRAME.to_sql(NOME_TABELA,
                         con = ENGINE,
                         schema = 'WSP',
                         if_exists = 'replace',
                         index = False,                
                        )
    except SQLAlchemyError as e:
        print(e)


# ## Função para baixar os dados no formato CSV

# In[38]:


def baixa_csv(DATAFRAME, NOME_TABELA):
    # Nessa etapa é importante colocar o caminho da pasta do SEU computador
    caminho = r'C:\\Users\\Gbrlm\\OneDrive - Grupo Portfolio\\Estudo\\Projetos\\Pokedex\\DadosCSV\\'
    DATAFRAME.to_csv(caminho + NOME_TABELA,
                     sep = ';',
                     index = False)


# # Dados Gerais dos Pokemon
# 
# _OBS: plural de pokemon = pokemon_
#     
# __Dados Coletados:__
# 1. ID na Pokedex
# 2. Nome
# 3. Tipo primário e secundário
# 4. Status base

# ## Scraping dos Dados
# 
# fonte: https://pokemondb.net/pokedex/all

# In[11]:


# Coletando o código html do site
html = captura_html('https://pokemondb.net/pokedex/all')
soup = BeautifulSoup(html)

# Coletando os IDs
IDs_raw = soup.find_all('span', {'class' : 'infocard-cell-data'})
IDs = [ID.contents[0] for ID in IDs_raw]
print(f'Foram coletados {len(IDs)} IDs')

# Coletando os nomes e tratando 
nomes_raw = soup.find_all('td', {'class' : 'cell-name'})
nomes = [nome.find('a', {'class' : 'ent-name'}).contents[0] if 'text-muted' not in str(nome) 
         else nome.find('small', {'class' : 'text-muted'}).contents[0] 
         if nome.find('a', {'class' : 'ent-name'}).contents[0] in nome.find('small', {'class' : 'text-muted'}).contents[0] 
         else nome.find('a', {'class' : 'ent-name'}).contents[0] + ' ' + nome.find('small', {'class' : 'text-muted'}).contents[0] 
         for nome in nomes_raw]
print(f'Foram coletados {len(nomes)} nomes')

# Criando lista de forma
lista_ids = []
formas = []
for i in range(len(IDs)):
    if IDs[i] not in lista_ids:
        lista_ids.append(IDs[i])
        formas.append('Base')
    else:
        formas.append('Alternativa')
        
print(f'Foram coletados {len(formas)} de formas alternativas ou bases')

# Coletando os tipos e adicionando tipos secudários quando existem
tipos_raw = soup.find_all('td', {'class' : 'cell-icon'})
tipos_raw_2 = [tipo.find_all('a') for tipo in tipos_raw]
tipos = [tipo[0].contents[0] + '/' + tipo[1].contents[0] if len(tipo) == 2 
         else tipo[0].contents[0] for tipo in tipos_raw_2]
print(f'Foram coletados {len(tipos)} tipos')

# Coletando os status
status_raw = soup.find_all('tr')
status_raw.pop(0)
hp = [int(status.find_all('td', {'class' : 'cell-num'})[1].contents[0]) for status in status_raw]
print(f'Foram coletados {len(hp)} dados de hp')
attack = [int(status.find_all('td', {'class' : 'cell-num'})[2].contents[0]) for status in status_raw]
print(f'Foram coletados {len(attack)} dados de attack')
defense = [int(status.find_all('td', {'class' : 'cell-num'})[3].contents[0]) for status in status_raw]
print(f'Foram coletados {len(defense)} dados de defense')
sp_atk = [int(status.find_all('td', {'class' : 'cell-num'})[4].contents[0]) for status in status_raw]
print(f'Foram coletados {len(sp_atk)} dados de sp_atk')
sp_def = [int(status.find_all('td', {'class' : 'cell-num'})[5].contents[0]) for status in status_raw]
print(f'Foram coletados {len(sp_def)} dados de sp_def')
speed = [int(status.find_all('td', {'class' : 'cell-num'})[6].contents[0]) for status in status_raw]
print(f'Foram coletados {len(speed)} dados de speed')


# ## Tratamento

# ### Criando dataframe com as listas coletadas

# In[12]:


df_geral = pd.DataFrame({
    'ID Pokedex' : IDs,
    'Nome' : nomes,
    'Forma' : formas,
    'Tipo' : tipos,
    'HP' : hp,
    'Attack' : attack,
    'Defense' : defense,
    'Sp.Atk' : sp_atk,
    'Sp.Def' : sp_def,
    'Speed': speed
})

df_geral.head()


# ### Criando coluna de total dos status

# In[13]:


df_geral['Total'] = (df_geral['HP'] + df_geral['Attack'] + df_geral['Defense'] 
                     + df_geral['Sp.Atk'] + df_geral['Sp.Def'] + df_geral['Speed'])


# ### Criando coluna com a geração de cada pokemon

# In[14]:


# ID do último pokemon de cada geração
ids = [151, 251, 386, 493, 649, 721, 809, 905]
geracoes = ['Gen 1', 'Gen 2', 'Gen 3', 'Gen 4', 'Gen 5', 'Gen 6', 'Gen 7', 'Gen 8']

# Percorrendo as listas e adcionando as gerações em outra lista
lista_geracoes = []
cont = 0
for ID in df_geral['ID Pokedex']:
    for i in range(len(ids)):
        if int(ID) <= ids[i]:
            lista_geracoes.append(geracoes[i])
            cont += 1
            break

# Criando coluna no dataframe
df_geral['Geração'] = lista_geracoes


# ### Traduzindo os tipos dos pokemon

# In[15]:


# Aplicando a função que traduz os tipos
df_geral['Tipo'] = [traduz_tipo(tipo) for tipo in df_geral['Tipo']]


# ### Separando a coluna de tipos em duas

# In[16]:


# Criando colunas novas
df_geral['Tipo 1'] = [tipo.split('/')[0] for tipo in df_geral['Tipo']]
df_geral['Tipo 2'] = [tipo.split('/')[1] if len(tipo.split('/')) == 2 else '-' for tipo in df_geral['Tipo']]

# Removendo coluna antiga
df_geral.drop(columns = ['Tipo'], inplace = True)


# # Imagens dos Pokemon
# 
# fonte: https://www.pokemon.com/br/pokedex/

# __padrão da url da imagem grande:__ 
# 1. Forma Base: https://assets.pokemon.com/assets/cms2/img/pokedex/full/ + __NUMERO_POKEDEX__ + .png
# 2. Forma Alternativa: https://assets.pokemon.com/assets/cms2/img/pokedex/full/ + __NUMERO_POKEDEX__ + _ + f + __NUMERO_FORMA__ + .png

# ## Criando dataframe auxiliar com a quantidade de formas por ID na Pokedex

# In[17]:


df_aux = df_geral.groupby(['ID Pokedex'])[['Forma']].count()
df_aux.rename(columns = {'Forma' : 'Qtd Formas por ID'}, inplace = True)
df_aux.head()


# ## Criando as URLs das imagens de cada pokemon

# In[18]:


url_base = 'https://assets.pokemon.com/assets/cms2/img/pokedex/full/'
lista_url = []
# Percorrendo o df_aux
for i in range(1, df_aux.shape[0] + 1):
    # Tratando o caso dos pokemon 'Darmanitan' e 'Rockruff'
    
    # Darmanitan 
    if i == 555:
        lista_url.append(url_base + '555.png')
        lista_url.append('https://img.pokemondb.net/artwork/darmanitan-zen.jpg')
        lista_url.append(url_base + '555_f2.png')
        lista_url.append('https://img.pokemondb.net/artwork/darmanitan-galarian-zen.jpg')
    # Rockruff
    elif i == 744:
        lista_url.append(url_base + '744.png')
        lista_url.append(url_base + '744.png')
    # Kyurem
    elif i == 646:
        lista_url.append(url_base + '646.png')
        lista_url.append(url_base + '646_f3.png')
        lista_url.append(url_base + '646_f2.png')
    # Pikachu
    elif i == 25:
        lista_url.append(url_base + '025.png')
        lista_url.append(r'https://img.pokemondb.net/artwork/pikachu-lets-go.jpg')
    # Eevee
    elif i == 133:
        lista_url.append(url_base + '133.png')
        lista_url.append(r'https://img.pokemondb.net/artwork/eevee-lets-go.jpg')
    else:
        for j in range(df_aux['Qtd Formas por ID'][i - 1]):
            if j == 0:
                lista_url.append(url_base + df_aux.index[i - 1] + '.png')
            else:
                lista_url.append(url_base + df_aux.index[i - 1] + '_f' + str(j + 1) + '.png')
print(f'Foram coletadas {len(lista_url)} imagens')


# In[19]:


# Adicionando a coluna com as imagens no dataframe geral
df_geral['URL Imagem'] = lista_url
df_geral.head()


# # Sprites dos Pokemon nos Jogos

# ## Extraindo URL da API de cada pokemon

# In[20]:


# URL com os pokemon
url = 'https://pokeapi.co/api/v2/pokemon/?limit=2000'

# Criando requisição para a API
response = requests.get(url)

# Transformando a resposta em dataframe (json -> dict python -> dataframe pandas)
encode = json.loads(response.text)
df_url = pd.DataFrame(encode['results'])
df_url.head()


# ## Extraindo sprites

# In[21]:


# Requisitando na API todas as URLs e coletando os sprites

df_sprites = pd.DataFrame()

for url in df_url['url']:

    # Criando requisição para a API
 
    response = requests.get(url)

    # Criando loop para cada resposta para coletar sprites de todas as geracoes
    encode = json.loads(response.text)
    
    # Verificando id limite
    if int(encode['id']) > 905:
        break
    
    geracoes = ['generation-i', 'generation-ii', 'generation-iii', 'generation-iv',
            'generation-v', 'generation-vi', 'generation-vii', 'generation-viii']
    
    df_aux = pd.DataFrame()

    for geracao in geracoes:

        # Extraindo sprites
        df = pd.DataFrame(encode['sprites']['versions'][geracao])

        if geracao == 'generation-i':
            df2 = df.loc[['front_default', 'front_gray']]
        elif geracao == 'generation-viii':
            df2 = df.loc[['front_default']]
        else:
            df2 = df.loc[['front_default', 'front_shiny']]

        # Adicionando dados no auxiliar
        for i in range(df2.shape[1]):
            num_coluna = i
             
            df_aux = pd.concat([df_aux, df2.iloc[:, num_coluna]])
    # Tratando id do pokemon para ficar com 3 digitos
    id_pokedex = str(encode['id'])
    while len(id_pokedex) < 3:
        id_pokedex = '0' + id_pokedex
            
    # Adicionando dados no dataframe principal e criando coluna com o id do pokemon
    
    df_aux['ID Pokédex'] = id_pokedex
    df_sprites = pd.concat([df_sprites, df_aux])
    
# Mostrando o dataframe 
df_sprites.head()


# ## Tratando o dataframe coletado

# In[22]:


# Removendo valores nulos 
df_sprites.dropna(inplace = True)

# Renomeando coluna com as urls
df_sprites.rename(columns = {0 : 'Url_sprite'}, inplace = True)

# Criado coluna para identificar a forma (normal/shiny/preto e branco)
df_sprites['Forma'] = ''

df_sprites.loc['front_gray', 'Forma'] = 'Preto e Branco'
df_sprites.loc['front_default', 'Forma'] = 'Normal'
df_sprites.loc['front_shiny', 'Forma'] = 'Shiny'

df_sprites.head()


# # Status dos Pokemon

# ## Extraindo dataframe com os status do dataframe geral

# In[23]:


dados = []
for i in range(len(df_geral)):
    dados.append((1, df_geral['URL Imagem'][i], df_geral['Forma'][i], 'HP', df_geral['HP'][i]))
    dados.append((2, df_geral['URL Imagem'][i], df_geral['Forma'][i], 'Attack', df_geral['Attack'][i]))
    dados.append((3, df_geral['URL Imagem'][i], df_geral['Forma'][i], 'Defense', df_geral['Defense'][i]))
    dados.append((4, df_geral['URL Imagem'][i], df_geral['Forma'][i], 'Sp.Atk', df_geral['Sp.Atk'][i]))
    dados.append((5, df_geral['URL Imagem'][i], df_geral['Forma'][i], 'Sp.Def', df_geral['Sp.Def'][i]))
    dados.append((6, df_geral['URL Imagem'][i], df_geral['Forma'][i], 'Speed', df_geral['Speed'][i]))
    dados.append((7, df_geral['URL Imagem'][i], df_geral['Forma'][i], 'Total', df_geral['Total'][i]))
    
# Montando df_status
df_status = pd.DataFrame(dados, columns = ['Ordenador', 'URL Imagem', 'Forma', 'Status', 'Valor'])

# Removendo colunas no dataframe principal
df_geral.drop(columns = ['HP', 'Attack', 'Defense', 'Sp.Atk', 'Sp.Def', 'Speed'], inplace = True)

# Mostrando df_status
df_status.head()


# # Ataques dos Pokemon

# ## Coletando ID e Link para a página individual de cada pokemon

# In[24]:


# Coletando o código html do site
html = captura_html('https://pokemondb.net/pokedex/all')
soup = BeautifulSoup(html)

# Coletando os IDs
IDs_raw = soup.find_all('span', {'class' : 'infocard-cell-data'})
IDs = [ID.contents[0] for ID in IDs_raw]
print(f'Foram coletados {len(IDs)} IDs')

# Coletando os Links
links_raw = soup.find_all('a', {'class' : 'ent-name'})
links = ['https://pokemondb.net' + link.get('href') for link in links_raw]
print(f'Foram coletados {len(links)} links')


# In[25]:


# Monstando dataframe com os IDs e os Links
df_links = pd.DataFrame({
    'ID Pokedex' : IDs,
    'Link' : links
})

# Como alguns pokemons possuem mais de uma forma, é necessário remover os links duplicados
df_links.drop_duplicates(subset = 'ID Pokedex', inplace = True)
df_links.reset_index(drop = True, inplace = True)

# Mostrando df_links
df_links.head()


# ## Percorrendo todos os links e capturando todos os ataques em dois dataframes
# 
# __DataFrames:__ 
# 1. df_tm: Ataques que podem ser ensinados ao pokemon
# 2. df_level: Ataques que o pokemon aprende ao subir de nível

# In[26]:


lista_df_tm = []
lista_df_level = []
cont = 0
# Percorrendo os links coletados
for i in range(len(df_links)):
    cont += 1
    if cont % 100 == 0:
            print(f'Foram coletados os ataques de {cont} pokemon\n')
            
    # Coletando os ataques por nível de cada pokemon
    try:
        mini_df_level = pd.read_html(captura_html(df_links['Link'][i]), match = 'Lv.')[0]
        mini_df_level['ID Pokedex'] = df_links['ID Pokedex'][i]
        lista_df_level.append(mini_df_level)
    except ValueError as e:
        print(e)
        print(f'O pokemon com o link {df_links["Link"][i]} não aprende golpes por nível, ou aconteceu algum erro\n')
 
    # Coletando os ataques que podem ser ensinados
    try:
        mini_df_tm = pd.read_html(captura_html(df_links['Link'][i]), match = re.compile(r'\bTM\b'))[0]
        mini_df_tm['ID Pokedex'] = df_links['ID Pokedex'][i]
        lista_df_tm.append(mini_df_tm)
    except ValueError as e:
        print(e)
        print(f'O pokemon com o link {df_links["Link"][i]} não aprende golpes por TM, ou aconteceu algum erro\n')
        
# Unindo todos os dataframes individuais de cada pokemon
df_tm = pd.concat(lista_df_tm)
df_level = pd.concat(lista_df_level)


# ## Tratando os dataframes criados

# ### Dataframe com os ataques ensináveis 

# In[27]:


# Visualizando o dataframe 
df_tm.head()


# In[28]:


# Removendo colunas indesejadas
df_tm.drop(columns = ['Cat.'], inplace = True)

# Mudando o nome da coluna de tipos e traduzindo os tipos
df_tm.rename(columns = {'Type' : 'Tipo', 
                        'Move' : 'Ataque', 
                        'Acc.' : 'Precisão(%)', 
                        'Power' : 'Dano'}, inplace = True)

df_tm['Tipo'] = [traduz_tipo(tipo) for tipo in df_tm['Tipo']]

# Visualizando o dataframe
df_tm.head()


# ### Dataframe com os ataques por nível

# In[29]:


# Visualizando o dataframe 
df_level.head()


# In[30]:


# Removendo colunas indesejadas
df_level.drop(columns = ['Cat.'], inplace = True)

# Mudando o nome da coluna de tipos e traduzindo os tipos
df_level.rename(columns = {'Type' : 'Tipo', 
                           'Move' : 'Ataque', 
                           'Acc.' : 'Precisão(%)', 
                           'Power' : 'Dano',
                           'Lv.' : 'Nível'}, inplace = True)

df_level['Tipo'] = [traduz_tipo(tipo) for tipo in df_level['Tipo']]

# Visualizando o dataframe
df_level.head()


# In[31]:


# Total de ataques capturados
print(f'Foram capturados um total de {len(df_tm) + len(df_level)} ataques')


# # Evoluções dos Pokemon

# ## Coleta dos Dados

# In[32]:


# Coletando HTML do site 
soup = BeautifulSoup(captura_html('https://pokemon.fandom.com/wiki/List_of_Pok%C3%A9mon_by_evolution'))

# Indetificando tabela no HTML e capturando as linhas
tabela = soup.find('table', {'style' : 'border-collapse:collapse;'})
linhas_raw = tabela.find_all('tr')

dados_evo = []

cont = 0
for linha_raw in linhas_raw:
    estagios = linha_raw.find_all('td')
    if cont == 0:
        cont += 1
    else:
        # Coletando os pokemons de cada linha e separando em estágios
        estagio_1 = estagios[1].find('a').contents[0]
        estagios_2 = [estagio.contents[0] for estagio in estagios[2].find_all('a')]
        estagios_3 = [estagio.contents[0] for estagio in estagios[3].find_all('a')]
        
        # Criando cadeias evolutivas formatadas
        
        # Pokemon não evolui
        if len(estagios_2) == 0:
            linha = (estagio_1, '-', '-')
            print(linha)
            dados_evo.append(linha)

        # Cadeias lineares com 3 etapas (1-1-1)
        if len(estagios_2) == 1 and len(estagios_3) == 1:
            linha = (estagio_1, estagios_2[0], estagios_3[0])
            print(linha)
            dados_evo.append(linha)
            
        # Cadeias lineares com 2 etapas (1-1-0)
        elif len(estagios_2) == 1 and len(estagios_3) == 0:
            linha = (estagio_1, estagios_2[0], '-')
            print(linha)
            dados_evo.append(linha)
            
        # Cadeias ramificadas com 2 etapas (1-x)
        elif len(estagios_2) > 1 and len(estagios_3) == 0:
            for pkmn in estagios_2:
                linha = (estagio_1, pkmn, '-')
                print(linha)
                dados_evo.append(linha)
                
        # Cadeias ramificadas com 3 etapas I (1-1-x)
        elif len(estagios_2) == 1 and len(estagios_3) > 1:
            for pkmn in estagios_3:
                linha = (estagio_1, estagios_2[0], pkmn)
                print(linha)
                dados_evo.append(linha)
        
        # Cadeias ramificadas com 3 etapas II (1-2-2)
        elif len(estagios_2) == 2 and len(estagios_3) == 2:
            for i in range(2):
                linha = (estagio_1, estagios_2[i], estagios_3[i])
                print(linha)
                dados_evo.append(linha)
                
        


# In[33]:


# Criando dataframe com os dados coletados
df_evo_0 = pd.DataFrame(dados_evo, columns = ['estagio_1', 'estagio_2', 'estagio_3'])
df_evo_0.head()


# ## Aplicando tratamento aos dados coletados

# In[34]:


# Criando dois dataframes a partir do coletado
df_evo_1 = pd.DataFrame({'Pokemon' : df_evo_0['estagio_1'],
                         'Evolução' : df_evo_0['estagio_2']})
df_evo_2 = pd.DataFrame({'Pokemon' : df_evo_0['estagio_2'],
                         'Evolução' : df_evo_0['estagio_3']})

# Unindo os dataframes criados
df_evo = pd.concat([df_evo_1, df_evo_2])
df_evo.drop_duplicates(subset = 'Evolução', inplace = True)

# Adicionando o ID de cada pokemon
df_evo = df_evo.merge(df_geral.loc[:, ['ID Pokedex', 'Nome']], left_on = 'Pokemon', right_on = 'Nome', how = 'left')
df_evo.drop(columns = ['Nome'], inplace = True)
df_evo.rename(columns = {'ID Pokedex' : 'ID Pokemon'}, inplace = True)

# Adicionando ID de cada evolução
df_evo = df_evo.merge(df_geral.loc[:, ['ID Pokedex', 'Nome']], left_on = 'Evolução', right_on = 'Nome', how = 'left')
df_evo.drop(columns = ['Nome'], inplace = True)
df_evo.rename(columns = {'ID Pokedex' : 'ID Evolução'}, inplace = True)

# Reordenando dataframe e mostrando
df_evo = df_evo[['ID Pokemon', 'Pokemon', 'ID Evolução', 'Evolução']]
df_evo.head()


# # Carregando dados

# ## Criando conexão com o banco

# In[35]:


try:
    engine = create_engine('postgresql+psycopg2://postgres:ash@pikachu/pokedex') # Credenciais alteradas por segurança
    print('Conexão OK!')
except SQLAlchemyError as e:
    print(e)


# ## Subindo tabelas para o banco

# In[36]:


# Dataframe com dados gerais
envia_postgres(df_geral.loc[df_geral['Forma'] == 'Base'], engine, 'dados_gerais_base')
envia_postgres(df_geral.loc[df_geral['Forma'] == 'Alternativa'], engine, 'dados_gerais_alt')

# Dataframes com os status
envia_postgres(df_status.loc[df_status['Forma'] == 'Base'], engine, 'status_base')
envia_postgres(df_status.loc[df_status['Forma'] == 'Alternativa'], engine, 'status_alt')

# Dataframes com os ataques
envia_postgres(df_tm, engine, 'ataques_TM')
envia_postgres(df_level, engine, 'ataques_Level')

# Dataframe com as evoluções
envia_postgres(df_evo, engine, 'evolucoes')

# Dataframe com os sprites
envia_postgres(df_sprites, engine, 'sprites')


# # Baixando dados no formato CSV para disponibilização

# In[39]:


# Dataframe com dados gerais
baixa_csv(df_geral, 'dados_gerais')

# Dataframes com os status
baixa_csv(df_status, 'status')

# Dataframes com os ataques
baixa_csv(df_tm, 'Ataques_TM')
baixa_csv(df_level, 'ataques_Level')

# Dataframe com as evoluções
baixa_csv(df_evo, 'evolucoes')

# Dataframe com os sprites
baixa_csv(df_sprites, 'sprites')

