# PowerDex, a pokédex feita com Python e Power BI!

![Banner Inicial](https://user-images.githubusercontent.com/110268371/183133088-8c64acf9-a406-4dfb-a80d-dea0345409be.png)

<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=Finalizado&color=GREEN&style=for-the-badge"/>
</p>

Link para o projeto: https://bit.ly/Powedex

# 🧾Descrição do Projeto

Projeto em desenvolvimento com o objetivo de por em prática conhecimentos em ETL que vão desde a extração e tratamento dos dados via Python e visualização via Power BI

A Power Dex permite a consulta de informações sobre os pokémon lançados até a 8° geração como status base, evoluções, formas alternativas, movimentos e muito mais

![fluxograma do projeto](https://user-images.githubusercontent.com/110268371/183149732-21fad29b-95c9-497d-af3d-e4aaa9733603.png)

# 🛠️Ferramentas e Tecnologias

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" height="40"/>     <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="40" height="40"/> <img src="https://user-images.githubusercontent.com/110268371/183156168-290db6e2-b5a8-40b7-bf72-fdde1d78c0b2.png" width="32" height="40"/>

# 🛠️Funcionalidades

## Página de dados gerais 

- `Funcionalidade 1`: Cores do dashboard são variáveis, dependendo do tipo do pokémon em análise

- `Funcionalidade 2`: Consulta dos dados básicos do pokémon

- `Funcionalidade 3`: Visualização de imagens do pokémon, que incluem: Imagem oficial do pokemon, sprite do pokémon nos jogos da série, imagem das formas alternativas e imagem da sua evolução

![Dados Gerais Pikachu](https://user-images.githubusercontent.com/110268371/183152160-ee0246f8-b187-42f3-892a-344d3d71b40b.png) 

- `Funcionalidade 4`: Pop-ups para melhor visulização das formas alternativas e evoluções

![pop-ups](https://user-images.githubusercontent.com/110268371/183159484-23f105af-b1b1-4e76-b4f7-a9067512e886.png)

- `Funcionalidade 5`: Filtro para escolha do pokémon

![Filtro pokémon](https://user-images.githubusercontent.com/110268371/183152505-178fbb82-9782-46b9-88d7-62bf092a4819.png)

## Página de movimentos

- `Funcionalidade 1`: Informação sobre em que nível um pokémon aprende determinado movimento
- `Funcionalidade 2`: Informação sobre quais TMs um pokémon pode aprender

![Movimentos Bulbassauro](https://user-images.githubusercontent.com/110268371/183154031-5b3419ed-97fc-4bf1-ae00-3ed6a1dff66a.png)

## Página de análise

- `Funcionalidade 1`: Comparação da quantidade de pokémon por Tipo e por Geração
- `Funcionalidade 2`: Ranking dos status dos pokémon
- `Funcionalidade 3`: Filtro por tipo primário, tipo secundário, geração e status

![Página de análisee](https://user-images.githubusercontent.com/110268371/183156795-83394e48-5282-46ab-b770-534b0e00569b.png)

- `Funcionalidade 4`: Pop-ups para visulização dos pokémon filtrados em TODOS os gráficos

![Filtro fogo](https://user-images.githubusercontent.com/110268371/183158362-e9853854-106d-4d7e-b875-4b69bbce23f3.png)

# 🧾Descrição das Ferramentas Utilizadas

## 🥄Coleta dos dados

### Web Scraping

#### Fontes:
<p>Dados gerais e Movimentos: <a href="https://pokemondb.net/" target="_blank">Pokémon Database</a></p>
<p>Imagens dos Pokémon e suas Formas Alternativas: <a href="https://www.pokemon.com/br/" target="_blank">Site Oficial do Pokémon</a></p>
<p>Evoluções dos Pokémon: <a href="https://pokemon.fandom.com/wiki/Pok%C3%A9mon_Wiki" target="_blank">Pokémon Fandom Wiki</a></p>


#### 🧾Descrição do processo:
![image](https://user-images.githubusercontent.com/110268371/183217147-138c127c-73e6-45b8-a7f7-ae3ae3c522a1.png)

A coleta dos dados citados acima foi possível graças à construção de um algorítmo de Web Scraping / Web Crawling em <a href="https://www.python.org/" target="_blank">Python 🐍</a>.

Para isso, fiz a requisição com a URL do site onde estavam as informações desejadas utilizando a biblioteca <a href="https://docs.python.org/3/library/urllib.html" target="_blank">urllib</a>, que me devolveu o código HTML completo do site. Após isso, esse código HTML é decodificado por outra biblioteca, chamada <a href="https://beautiful-soup-4.readthedocs.io/en/latest/#" target="_blank">Beautiful Soup 🍲</a>, que cria um objeto python navegável onde eu posso buscar as informações.

Para buscar as informações, grande parte pode ser capturada usando funções da própria biblioteca Beautiful Soup, mas outras precisaram do uso de um pacote python chamado <a href="https://docs.python.org/3/library/re.html" target="_blank">RE</a>, que torna possível o uso de expressões regulares em Python.

### PokéAPI

#### Fontes:
<p>API de onde foram extraídos os sprites nos jogos: <a href="https://pokeapi.co/" target="_blank">PokéAPI</a></p>


#### 🧾Descrição do processo:
![image](https://user-images.githubusercontent.com/110268371/183217177-a0cc3274-23de-4f73-9c7a-88f349614117.png)

A <a href="https://pokeapi.co/" target="_blank">PokéAPI</a> é uma API pública muito completa, lá estão quase todos os dados possíveis de cada pokémon e item dos jogos da franquia  <i>(O projeto inclusive poderia ser feito inteiramente com dados dessa API, mas um dos objetivos era praticar coleta de dados via Web Scraping)</i>.

Para capturar os dados foi utilizada a biblioteca <a href="https://pypi.org/project/requests/" target="_blank">Requests</a> para fazer as requisições para a API , e o modulo python <a href="https://docs.python.org/3/library/json.html" target="_blank">Json</a> para transformar a resposta da API (JSON) para dicionário Python.


## 🥣Tratamento e carregamento dos dados
![image](https://user-images.githubusercontent.com/110268371/183217058-f7f855be-82a6-42c8-bc4c-30f738d86053.png)


O tratamento dos dados foi feito intreiramente em Python, usando a biblioteca <a href="https://pandas.pydata.org/docs/" target="_blank">Pandas 🐼</a>, que nos permite realizar o tratamento dos dados de forma eficiente.

Para carregar os dados foi utilizada uma combinação entre funções da biblioteca Pandas e da biblioteca <a href="https://www.sqlalchemy.org/" target="_blank">SQLAlchemy ⚗️</a>, que possui a capacidade de se comunicar com a vasta maioria dos bancos de dados de forma simples e eficiente, permitindo tanto o carregamento dos dados, quanto a possibilidade de fazer <i>queries SQL</i> (consultas ao banco).

Falando em banco de dados, o escolhido para esse projeto foi o <a href="https://www.postgresql.org/" target="_blank">PostegreSQL 🐘</a> por ser um banco de dados relacional muito robusto e por ser <i>Open Source</i>. Após o carregamento para o banco de dados, os dados foram consultados no <a href="https://powerbi.microsoft.com/pt-br/" target="_blank">Power BI</a>, onde foi desenvolvida toda a parte visual.

# 🧑‍🍳ETL

## 🥄Extract - Extração dos Dados
<i>OBS: Todos os dados coletados foram armazenados em dataframes Pandas</i>
### Web Scraping
- `Dados Gerais`: Foram coletados da <a href="https://pokemondb.net/pokedex/all" target="_blank">página de status da pokemon db</a>, os seguintes dados: nome, id, tipo (completo), status, forma (base ou alternativa) e link para a página de cada pokemon.

- `Ataques/Movimentos`: Foi coletado da página individual de cada pokémon (Ex: <a href="https://pokemondb.net/pokedex/pikachu" target="_blank">Pikachu</a>), informações sobre todos os movimentos que um pokémon pode aprender, seja por TM, seja por nível.

- `Evoluções`: Da <a href="https://pokemon.fandom.com/wiki/List_of_Pok%C3%A9mon_by_evolution" target="_blank">página de cadeias evolutivas da pokemon fandom wiki</a>, foram coletados os nomes dos pokemons dos estágios 1, 2 e 3 de cada linha evolutiva.

### API
- `Sprites`: da <a href="https://pokeapi.co/" target="_blank">PokéAPI</a> foram extraídos os links para as imagens de como os pokémon aparecem nos jogos da franquia.

## 🥣Transform - Transformação/Tratamento dos dados
<i>OBS: Todos os dados foram tratados utilizando apenas funções da biblioteca Pandas e do próprio Python</i>

- `Tipos`: A coluna coletada com os tipos completos dos pokémon foi traduzida para o português e foi dividida em duas colunas (Tipo Primário e Tipo Secundário). (Ex:
Tipo: Grass/Poison >>> Tipo 1: Planta / Tipo 2: Veneno).

- `Geração`: Foi adicionada uma coluna com a geração de cada pokemon, baseada no seu ID.

- `Imagem`: Foi criada uma coluna com o link da imagem oficial de cada pokémon disponível no <a href="https://www.pokemon.com/br/" target="_blank">Site Oficial do Pokémon</a>, utilizando apenas um padrão que depende do ID.
     - Forma Base: https://assets.pokemon.com/assets/cms2/img/pokedex/full/ + __ID_POKEDEX__ + .png
     - Forma Alternativa: https://assets.pokemon.com/assets/cms2/img/pokedex/full/ + __ID_POKEDEX__ + _ + f + __NUMERO_FORMA__ + .png
     
- `Status`: No dataframe inicial havia uma coluna para cada status do pokémon, desse dataframe, foi extraído outro dataframe com uma coluna definindo o status, uma coluna com o valor do status, a URL de cada pokémon, a forma e a ordenação de cada status.

- `Ataques/Movimentos`: Tanto no dataframe com os movimentos por TM, quanto no dataframe com os movimentos por nível, foram traduzidos os tipos dos movimentos, foram traduzidas todas as colunas (Ex: Acc. >>> Precisão(%)) e foi removida a coluna "Cat.", que continha uma imagem que descrevia cada movimento.

## 🥗Load - Carregamento dos dados
### PostgreSQL
<i>OBS: Dados carregados para o banco usando a Pandas e SQLAlchemy.</i>

### CSV
Os dados também foram carregados para arquivos CSV, com o objetivo de facilitar a disponibilização do dataset coletado.



