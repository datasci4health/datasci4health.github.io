# E2 - Segunda Entrega - 2023.1 Ciência e Visualização de Dados em Saúde

O objetivo geral do projeto final desta disciplina é realizar a análise de dados relacionados à saúde, para usá-los em uma das seguintes possíveis tarefas: recomendação, estudo de associações, validação de hipóteses, análise exploratória, análise visual, análise comparativa e predição.

Na segunda entrega do projeto, seu grupo deverá:

  - Atualizar o repositório GitHub já criado anteriormente com informações e códigos associados à etapa de análise exploratória de dados (fork do repositório da disciplina);
 - O arquivo README.md do projeto deve ser atualizado para conter as seções do template abaixo.
 - Todos os scripts ou arquivos de processamento dos dados até o momento devem ser disponibilizados nas pastas correspondentes.
 - Após a finalização da edição do conteúdo da segunda entrega, atribuir a tag de release **2023.1_datasci4health_E2**.
 - Dar um  **pull request**  do projeto no  **branch  principal** até a data de entrega.
# Estrutura do Repositório
A fim de uniformizar os repositórios de projetos da disciplina, os diretórios de seu repositório deverão ser nomeados e utilizados segundo a estrutura sugerida em [Home - Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/), na seção "Directory structure".

Note que nem todos os diretórios ou arquivos serão necessários para todos os projetos. Foque em seguir o padrão para os diretórios que forem necessários. Não crie diretórios que não serão utilizados. Uma breve descrição dessa estrutura, com as pastas mais importantes é dada a seguir.

Seu repositório deverá obrigatoriamente conter o arquivo README.md, arquivo de documentação Markdown, que deverá conter a descrição do projeto conforme orientações a seguir.

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


# Orientações para Análise Exploratória em Geral

Em várias partes do modelo sugerido a seguir, será indicado que você apresente uma análise exploratória. Para cada um deles, seguem algumas orientações do que escrever:
 * use estatística descritiva e gráficos;
* inclua gráficos de sobre a distribuição dos dados (e.g., histogramas e boxplots);
* analise correlação e use gráficos de dispersão;
* descreva os resultados/gráficos, os analise e contextualize com o tema definido.

# Modelo para Apresentação do Projeto (Arquivo REAME.MD)

# Projeto `<Título em Português>`
# Project `<Title in English>`

# Apresentação

O presente projeto foi originado no contexto das atividades da disciplina de pós-graduação [*Ciência e Visualização de Dados em Saúde*](https://github.com/datasci4health/home), oferecida no primeiro semestre de 2023, na Unicamp.

> Incluir nome RA e foco de especialização de cada membro do grupo. Os grupos devem ter no máximo 5 integrantes e devem contar com pelo menos um aluno da área da saúde e um aluno de área afim à Computação (Ex.: Computação, Elétrica...)
> |Nome  | RA | Especialização|
> |--|--|--|
> | Nome1  | 123456  | Saúde|
> | Nome2  | 123456  | Computação - Líder Github - Conta <incluir login conta github>|
> | Nome3  | 123456  | XXX|
> | Nome4  | 123456  | XXX|
> | Nome5  | 123456  | XXX|

# Descrição Resumida do Projeto
> Descrição do tema do projeto, incluindo motivação e contexto gerador.
>
> Link para vídeo de apresentação da proposta do projeto (máximo 3 minutos) (Manter o mesmo da Entrega 1)

# Perguntas de Pesquisa
> Perguntas de pesquisa (revisadas e atualizadas) que o projeto pretende responder ou hipóteses a serem avaliadas, enunciadas de maneira objetiva e verificável.
> Se a análise exploratória contribuiu para as perguntas de pesquisa, apresente aqui elementos de análise exploratória que ajudem a responder a questão.

# Metodologia
> Proposta de metodologia incluindo especificação de quais técnicas pretende-se explorar, tais como: aprendizagem de máquina, análise de redes, análise estatística, ou integração de uma ou mais técnicas. Para a primeira entrega, descreva de maneira mais genérica que tipo de abordagem seu grupo pretende realizar.

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
> Inclua um sumário com estatísticas descritivas da(s) base(s) de estudo.
> Utilize gráficos que descrevam os aspectos principais da base que são relevantes para as perguntas de pesquisa consideradas.

# Ferramentas
> Ferramentas já utilizadas e/ou ainda a serem utilizadas (com base na visão atual do grupo sobre o projeto).

# Cronograma
> Atualização do cronograma.
