
# Projeto - Entrega Final

O objetivo geral do projeto final desta disciplina é realizar a análise de dados relacionados à saúde, para usá-los em uma das seguintes possíveis tarefas: recomendação, estudo de associações, validação de hipóteses, análise exploratória, análise visual, análise comparativa e predição.

A entrega final do projeto consiste em duas etapas: 
* Apresentação do Projeto (valendo 2,0 pontos): Vídeo de Apresentação entregue com o relatório + Arguição na data de apresentação (presença de todos os membros do grupo obrigatória)
* Relatório de Projeto (valendo 6,0 pontos).

## Datas Importantes

02/07 - Até 15:00h - Data e hora limites para última atualização do repositório do projeto (será considerada a última versão até essa data e horário).
02/07 - A partir das 16:00 (Presença obrigatória de todos os membros do grupo na data de apresentação. Requerida presença de todos os alunos da disciplina nas datas das apresentações).
13/07 - Até 10:00 - Entrega da avaliação por pares (vide outras informações abaixo).

## Instruções para o Relatório Final

Na entrega do relatório final do projeto, seu grupo deverá:

 - Complementar o repositório GitHub ou GitLab **público** já criado anteriormente com informações e códigos associados à uma implementação prática de uma análise. Por implementação entende-se a execução prática da análise usando um ou mais sistemas de análise e/ou o desenvolvimento de software para análise. 
 - Deve ser mantida a estrutura anterior do repositório conforme orientações da [Primeira Entrega](https://github.com/datasci4health/home/blob/master/resources/templates/entrega1.md). 
 - O arquivo README.md deve ser atualizado para conter as seções do template abaixo. 
 - Todos os scripts ou arquivos de processamento dos dados até o momento devem ser disponibilizados nas pastas correspondentes.

## Instruções para a Apresentação

A fim de garantirmos que será possível a apresentação de todos os grupos nas datas agendadas, as apresentações deverão ser gravadas e entregues junto com o relatório final em lugar destacado no template do relatório.

No dia da arguição do grupo, o vídeo será tocado e serão reservados 5 minutos para perguntas dos professores e dos alunos da turma.

O vídeo pré-gravado deve ter no máximo 8 minutos e todos os membros do grupo devem participar da apresentação.

Diretrizes para apresentação (sugestões de tópicos): 
* Deve recapitular, de maneira sintética, objetivo inicial do projeto 
* Abordagem adotada 
* Dificuldades enfrentadas 
* Deve relatar possíveis mudanças de percurso 
* Referenciais teóricos adotados 
* Principais ferramentas utilizadas (incluir informações úteis para que outros possam utilizá-las) 
* Resultados obtidos 
* Discussão dos resultados 
* Conclusões / Lições aprendidas 
* Trabalhos futuros

## Avaliação

A avaliação do projeto final será realizada não apenas pelos professores da disciplina, mas também passará por etapa de avaliação por pares.


# Estrutura do Repositório

Manter estrutura anterior, vide orientações da [Primeira Entrega](https://github.com/datasci4health/home/blob/master/resources/templates/entrega1.md)

A fim de uniformizar os repositórios de projetos da disciplina, os diretórios de seu repositório deverão ser nomeados e utilizados segundo a estrutura sugerida em [Home - Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/), na seção "Directory structure".

A seguir é apresentada uma simplificação da proposta de [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) que também será aceita. A estrutura geral é a seguinte e será detalhada a seguir:

~~~
├── README.md          <- apresentação do projeto
│
├── data
│   ├── external       <- dados de terceiros
│   ├── interim        <- dados intermediários, e.g., resultado de transformação
│   ├── processed      <- dados finais usados para a modelagem
│   └── raw            <- dados originais sem modificações
│
├── notebooks          <- Jupyter notebooks ou equivalentes
│
├── src                <- fonte em linguagem de programação ou sistema (e.g., Orange)
│   └── README.md      <- instruções básicas de instalação/execução
│
└── assets             <- mídias usadas no projeto
~~~

Na raiz deve haver um arquivo de nome `README.md` contendo a apresentação do projeto, como detalhado na seção seguinte.

## `data`

Dados utilizados no projeto respeitadas as possíveis implicações éticas, se você tiver licença para tal e se o volume for suportado pelo Github. Você pode optar por colocar um subconjunto ilustrativo dos dados.

É importante que sejam colocados os dados originais (se for possível) para garantir a reprodutibilidade do processo. Os originais são colocados na subpasta `raw` se forem produzidos pela equipe e na subpasta `external` se forem de terceiros. Também podem ser colocados aqui dados intermediários (por exemplo, dados tratados, resumidos etc.) na pasta `interim`. Finalmente, coloque os dados finais que serviram de entrada para as suas análises na subpasta `processed`.

## `notebooks`

Código do seu projeto que pode ser executado online sem instalação de software, tal como um notebook em Jupyter ou equivalente.

## `src`

Código em alguma linguagem ou projeto em Orange, Weka e similares.

Se for código em linguagem de programação, tente organizá-lo de forma que seja simples a sua execução por terceiros, por exemplo, acrescente as bibliotecas necessárias etc. Acrescente na raiz um arquivo `README.md` com as instruções básicas de instalação e execução.

## `assets`

Qualquer mídia usada no seu projeto: vídeo, ilustrações, arquivos PDF etc.

Note que nem todos os diretórios ou arquivos serão necessários para todos os projetos. Foque em seguir o padrão para os diretórios que forem necessários. Não crie diretórios que não serão utilizados.

Seu repositório deverá obrigatoriamente conter o arquivo README.md, arquivo de documentação Markdown, que deverá conter a descrição do projeto conforme orientações a seguir.

# Editando Arquivo README.md

Este é um guia de como produzir documentação em Markdown. Para entender como criar documentos em Markdown no Github, veja o material/vídeo:
[Guia de Uso do Markdown](https://github.com/mc-unicamp/oficinas/tree/master/docs).

Vide detalhes sobre o Markdown em: [Mastering Markdown](https://guides.github.com/features/mastering-markdown/).

E mais especificamente sobre tabelas em: [Organizing information with tables](https://help.github.com/en/articles/organizing-information-with-tables)

Segue abaixo o modelo de como devem ser documentadas as entregas.
> Tudo o que aparece neste modo de citação, ou indicado entre `<...>`, se refere a algo que deve ser substituído pelo indicado. No modelo são colocados exemplos ilustrativos, que serão substituídos pelos do seu projeto.


# Modelo Relatório Final de Projeto

# Projeto `<Título em Português>`
# Project `<Title in English>`

# Apresentação

O presente projeto foi originado no contexto das atividades da disciplina de pós-graduação [*Ciência e Visualização de Dados em Saúde*](https://github.com/datasci4health/home), oferecida no primeiro semestre de 2021, na Unicamp.

> Incluir nome RA e foco de especialização de cada membro do grupo. Os grupos devem ter no máximo 5 integrantes e devem contar com pelo menos um aluno da área da saúde e um aluno de área afim à Computação (Ex.: Computação, Elétrica...)
> |Nome  | RA | Especialização|
> |--|--|--|
> | Nome1  | 123456  | Saúde|
> | Nome2  | 123456  | Computação|
> | Nome3  | 123456  | XXX|
> | Nome4  | 123456  | XXX|
> | Nome5  | 123456  | XXX|

# Descrição Resumida do Projeto
> Descrição do tema do projeto, incluindo motivação e contexto gerador.
>
> Link para vídeo de apresentação da proposta do projeto (máximo 3 minutos).
> *Link para vídeo da apresentação final do projeto (máximo 8 minutos). TODOS OS MEMBROS DO GRUPO DEVEM APARECER NO VÍDEO.*

# Introdução e Referenciais de Teóricos
> Contextualização do projeto
> Motivação
> Relevância
> Trabalhos relacionados

# Perguntas de Pesquisa
> Perguntas de pesquisa (revisadas e atualizadas) ou hipóteses a serem avaliadas, enunciadas de maneira objetiva e verificável.

# Metodologia
> Abordagem adotada pelo projeto na busca pela resposta às perguntas de pesquisa.
> Justificar teoricamente, sempre que possível, a metodologia adotada.

## Bases de Dados e Evolução
> Elencar bases de dados estudadas e/ou utilizadas no projeto, organizando em duas partes. Primeiro aquelas que foram estudadas, mas não serão usadas e em seguida as bases adotadas.

### Bases Estudadas mas Não Adotadas

> Para cada base, coloque uma mini-tabela no modelo a seguir e depois detalhamento sobre como ela foi analisada/usada, conforme exemplo a seguir.

Base de Dados | Endereço na Web | Resumo descritivo
----- | ----- | -----
Título da Base | http://base1.org/ | Breve resumo (duas ou três linhas) sobre a base.

> Faça uma descrição sobre o que concluiu sobre esta base. Sugere-se que respondam perguntas ou forneçam informações indicadas a seguir:
> * O que descobriu sobre esse banco?
> * Quais as transformações e tratamentos (e.g., dados faltantes e limpeza) feitos?
> * Por que este banco não foi adotado?
> * Apresente aqui uma Análise Exploratória (inicial) sobre esta base.

### Bases Estudadas e Adotadas

> Para cada base, coloque uma mini-tabela no modelo a seguir e depois detalhamento sobre como ela foi analisada/usada, conforme exemplo a seguir.

Base de Dados | Endereço na Web | Resumo descritivo
----- | ----- | -----
Título da Base | http://base1.org/ | Breve resumo (duas ou três linhas) sobre a base.

> Faça uma descrição sobre o que concluiu sobre esta base. Sugere-se que respondam perguntas ou forneçam informações indicadas a seguir:
> * Qual o esquema/dicionário desse banco (o formato é livre)?
> * O que descobriu sobre esse banco?
> * Quais as transformações e tratamentos (e.g., dados faltantes e limpeza) feitos?
> * Apresente aqui uma Análise Exploratória (inicial) sobre esta base.

### Integração entre Bases e Análise Exploratória

> Descreva etapas de integração de fontes de dados e apresente a seguir uma análise exploratória que envolva ambas.

> Resultados de Análise Exploratória
* use estatística descritiva e gráficos;
* inclua gráficos de sobre a distribuição dos dados (e.g., histogramas e boxplots);
* analise correlação e use gráficos de dispersão;
* descreva os resultados/gráficos, os analise e contextualize com o tema definido.


# Análises Realizadas
> Descrição detalhada das análises realizadas.

## Ferramentas
> Panorama das ferramentas utilizadas incluindo discussão sobre o uso das mesmas

# Resultados
> Descrição dos resultados mais importantes obtidos

# Discussão
> Discussão dos resultados. Relacionar os resultados com as perguntas de pesquisa ou hipóteses avaliadas.

# Conclusão
> Destacar as principais conclusões obtidas no desenvolvimento do projeto.
> Destacar os principais desafios enfrentados.
> Principais lições aprendidas.

# Trabalhos Futuros
> O que poderia ser melhorado se houvesse mais tempo?

# Referências Bibliográficas
> Lista de artigos, links e referências bibliográficas.
> Fiquem à vontade para escolher o padrão de referenciamento preferido pelo grupo.

