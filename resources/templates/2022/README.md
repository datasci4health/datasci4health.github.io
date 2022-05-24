# Templates das Entregas dos Projetos

Na entrega do relatório final do projeto, seu grupo deverá:

- Criar um repositório GitHub ou GitLab **público** que será usado ao longo de todo o projeto (o link deverá ser submetido na atividade correspondente no Google Classroom da disciplina);
- Organizar o repositório segundo a estrutura de diretórios proposta abaixo;
- Editar arquivos README.md do repositório segundo modelos descrito a seguir;
- Todos os scripts ou arquivos de processamento dos dados devem ser disponibilizados nas pastas correspondentes.

## Estrutura de Arquivos e Pastas

A seguir é apresentada a estrutura de pastas esperada para entrega dos projetos:

~~~
├── README.md  <- apresentação da equipe
│
├── p2   <- projeto p2
│
├── p3   <- projeto p3
│
└── p4   <- projeto p4
~~~

Cada template a seguir corresponde a uma entrega do trabalho:
* [Projeto P2](p2/README.md)
* [Projeto P3](p3/README.md)

Na raiz deve haver um arquivo de nome `README.md` contendo a apresentação da equipe, como detalhado na seção seguinte.

## `pX`

Arquivos e diretórios referentes à entrega de um projeto específico. Cada terá um template específico para a escrita do relatório, mas seguirá (dento do diretório `pX`) a estrutura a seguir:

# Estrutura dentro de cada diretório `pX`

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

Na raiz deve haver um arquivo de nome `README.md` contendo a apresentação do projeto, como detalhado na seção `Arquivo README.md da raiz`.

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

# Arquivo README.md da raiz

# Equipe `<Nome da Equipe>`

O presente projeto foi originado no contexto das atividades da disciplina de pós-graduação [*Ciência e Visualização de Dados em Saúde*](https://ds4h.org), oferecida no primeiro semestre de 2022, na Unicamp.

> Incluir nome RA e foco de especialização de cada membro do grupo. Os grupos devem ter no máximo 3 integrantes.
> |Nome  | RA | Especialização|
> |--|--|--|
> | Nome1  | 123456  | Saúde|
> | Nome2  | 123456  | Computação|
> | Nome3  | 123456  | XXX|
