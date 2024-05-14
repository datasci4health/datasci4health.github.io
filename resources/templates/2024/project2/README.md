# P2 - Template da Segunda Entrega
*2024.1 Ciência e Visualização de Dados em Saúde*

# Estrutura de sua pasta de projeto

A fim de uniformizar os repositórios de projetos da disciplina, os diretórios de seu repositório deverão ser nomeados conforme segue.

A estrutura aqui apresentada é uma simplificação daquela proposta pelo [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/). Também será aceito que o projeto adote a estrutura completa do Cookiecutter Data Science e isso será considerado um diferencial. A estrutura geral é a seguinte e será detalhada a seguir:

~~~
...
│
└── project2
    |
    ├── README.md  <- texto da Entrega 2 do projeto
    │
    ├── data
    │   ├── external       <- dados de terceiros em formato usado para entrada na transformação
    │   ├── interim        <- dados intermediários, e.g., resultado de transformação
    │   ├── processed      <- dados finais usados para a publicação
    │   └── raw            <- dados originais sem modificações
    │
    ├── pipelines
    │   ├── notebooks      <- Jupyter notebooks ou equivalentes
    │   └── workflows      <- workflows Orange ou equivalentes 
    |
    ├── src                <- fonte em linguagem de programação ou sistema (e.g., Orange, Cytoscape)
    │   └── README.md      <- instruções básicas de instalação/execução
    │
    └── assets             <- mídias usadas no projeto
        ├── images  <- imagens usadas no texto do README.md
        └── slides  <- slides da prévia (em PDF)
~~~

Na raiz da pasta `project2` deve haver um arquivo de nome `README.md` contendo a apresentação do projeto, como detalhado na seção seguinte.

## `data`

Arquivos de dados usados no projeto, quando isso ocorrer.

## `pipelines`

Processos implementados no projeto que tenham sido executados em algum mecanismo de notebook, como o Jupyter, ou de workflow, como o Orange.

Dentro da pasta notebooks, podem ser apresentadas sequências de queries em Cypher usando o markdown. Posteriormente, será demonstrado como colocar essas queries em um notebook.

## `src`

Projeto na linguagem escolhida caso não seja usado o notebook, incluindo todos os arquivos de dados e bibliotecas necessários para a sua execução. Só coloque código Pyhton ou Java aqui se ele não rodar dentro do notebook.

Acrescente na raiz um arquivo `README.md` com as instruções básicas de instalação e execução.

## `assets`

Qualquer mídia usada no seu projeto: vídeo, imagens, animações, slides etc. Coloque os arquivos aqui (mesmo que você mantenha uma cópia no diretório do código).

Segue abaixo o modelo de como deve ser apresentado e documentado o projeto. Há partes do modelo a seguir que têm uma marcação específica indicando que **não devem ser literalmente transcritas**:

Trecho entre `<...>` representa algo que deve ser substituído pelo indicado. Nesse caso, você não deve manter os símbolos `<...>`.
> Parágrafos que aparecem neste modo de citação representa algo que deve ser substituído pelo explicado.

No modelo a seguir são colocados exemplos ilustrativos, que serão substituídos pelos do seu projeto.

> # Modelo para Apresentação da Entrega 2 do Projeto (Arquivo README.md)

# Projeto `<Título em Português>`
# Project `<Title in English>`

# Descrição Resumida do Projeto

> Descrição do tema do projeto, incluindo motivação e contexto gerador.

# Slides

> Coloque aqui o link para o PDF da apresentação da parte 2.

# Fundamentação Teórica

> Fundamentação teórica do problema em saúde/biologia. Cite artigos tomados como base e em que problema.

# Perguntas de Pesquisa
> Perguntas de pesquisa (revisadas e atualizadas) que o projeto pretende responder ou hipóteses a serem avaliadas, enunciadas de maneira objetiva e verificável.
> Se o estágio atual do projeto contribuiu para as perguntas de pesquisa, apresente aqui elementos dele que ajudem a responder a questão.

# Metodologia
> Proposta de metodologia incluindo especificação de quais de Ciência de Redes que estão sendo usadas no projeto,
> tais como: detecção de comunidades, análise de centralidade, predição de links, ou a combinação de uma ou mais técnicas. Descreva o que perguntas pretende endereçar com a técnica escolhida.

## Bases de Dados e Evolução

> Para cada base, coloque uma entrada na tabela no modelo a seguir e depois detalhamento sobre como ela foi analisada/usada, conforme exemplo a seguir.

> Base de Dados | Endereço na Web | Resumo descritivo
> ----- | ----- | -----
> Título da Base 1 | http://base1.org/ | Breve resumo (duas ou três linhas) sobre a base.
> Título da Base 2 | http://base2.org/ | Breve resumo (duas ou três linhas) sobre a base.

> Faça uma descrição sobre o que concluiu sobre esta base. Sugere-se que respondam perguntas ou forneçam informações indicadas a seguir:
> * O que descobriu sobre essa base?
> * Quais as transformações e tratamentos (e.g., dados faltantes e limpeza) feitos?

## Modelo Lógico

> Modelo lógico da base de grafos revisado. Para o modelo de grafos de propriedades, utilize este
> [modelo de base](https://docs.google.com/presentation/d/10RN7bDKUka_Ro2_41WyEE76Wxm4AioiJOrsh6BRY3Kk/edit?usp=sharing) para construir o seu.
> Coloque a imagem do PNG do seu modelo lógico como ilustrado abaixo (a imagem estará na pasta `image`):
>
> ![Modelo Lógico de Grafos](images/modelo-logico-grafos.png)

## Integração entre Bases

> Descreva se houve desafios de integração de fontes de dados.

## Análise Preliminar

> Este item não é obrigatório neste estágio. Apresente aqui uma análise preliminar dos dados se houver.
> Utilize gráficos que descrevam os aspectos principais da base que são relevantes para as perguntas de pesquisa consideradas.

## Evolução do Projeto
> Este item não é obrigatório neste estágio, mas pode ser uma preparação para o estágio final.
> Relatório de evolução, descrevendo as evoluções na modelagem do projeto, dificuldades enfrentadas, mudanças de rumo, melhorias e lições aprendidas. Referências aos diagramas, modelos e recortes de mudanças são bem-vindos.
> Podem ser apresentados destaques na evolução dos modelos conceitual e lógico. O modelo inicial e intermediários (quando relevantes) e explicação de refinamentos, mudanças ou evolução do projeto que fundamentaram as decisões.
> Relatar o processo para se alcançar os resultados é tão importante quanto os resultados.

# Ferramentas

> Ferramentas já utilizadas e/ou ainda a serem utilizadas (com base na visão atual do grupo sobre o projeto).

# Referências Bibliográficas

> Lista de artigos, links e referências bibliográficas.
>
> Fiquem à vontade para escolher o padrão de referenciamento preferido pelo grupo.