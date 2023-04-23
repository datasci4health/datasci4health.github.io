# E1 - Primeira Entrega - 2023.1 Ciência e Visualização de Dados em Saúde

O objetivo geral do projeto final desta disciplina é realizar a análise de dados relacionados à saúde, para usá-los em uma das seguintes possíveis tarefas: recomendação, estudo de associações, validação de hipóteses, análise exploratória, análise visual, análise comparativa e predição.

Na primeira entrega do projeto, seu grupo deverá:

 - Escolher um líder Github que ficará responsável pela administração do repositório. O líder, obrigatoriamente deverá ter poder de administração de uma conta Github;
 - Fazer um **fork** do [repositório de projetos da disciplina](https://github.com/datasci4health/projects2023) na conta Github;
 - Criar uma pasta com um nome que referencie seu projeto na raiz do novo repositório;
 - Iniciar a organização da pasta de projeto como descrito na Seção [Estrutura de sua pasta de projeto](#estrutura-de-sua-pasta-de-projeto);
 - Dentro da pasta criada, editar arquivo README.md do repositório com a proposta inicial do projeto, segundo modelo descrito na Seção [Modelo para Apresentação do Projeto](#modelo-para-apresentação-do-projeto);
 - Após a finalização da edição do conteúdo da primeira entrega, atribuir a tag de release **2023.1_datasci4health_E1** à versão atual do seu projeto;
 - Dar um **pull request** do projeto no **branch** principal até a data de entrega.


Após a primeira entrega, será agendada (em horário de aula) uma data de arguição da proposta de projeto. 
É obrigatória a participação de todos os membros durante o momento da arguição da proposta. 
Durante a arguição, os professores fornecerão feedbacks sobre a proposta e seu grupo poderá tirar dǘvidas sobre o encaminhamento do projeto. 

O objetivo geral do projeto final desta disciplina é realizar a análise de dados relacionados à saúde, para usá-los em uma das seguintes possíveis tarefas: recomendação, estudo de associações, validação de hipóteses, análise exploratória, análise visual, análise comparativa e predição.

Na primeira entrega do projeto, seu grupo deverá:

 - Escolher um líder Github que ficará responsável pela administração do repositório. O líder, obrigatoriamente deverá ter poder de administração de um conta Github;
 - Fazer um fork do repositório na conta Github;
 - Criar uma pasta com um nome que referencie seu projeto na raiz do novo repositório;
 - Dentro da pasta criada, editar arquivo README.md do repositório com a proposta inicial do projeto, segundo modelo descrito a seguir;
 - Disponibilizar vídeo de duração máxima de 3 minutos de apresentação da proposta do projeto. Não é necessário que todos os membros da equipe apareçam ou participem do vídeo.

Após a primeira entrega, será agendada (em horário de aula) uma data de arguição da proposta de projeto. 
É obrigatória a participação de todos os membros durante o momento da arguição da proposta. 
Durante a arguição, os professores fornecerão feedbacks sobre a proposta e seu grupo poderá tirar dǘvidas sobre o encaminhamento do projeto. 

# Estrutura de sua pasta de projeto

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


# Editando Arquivo README.md

Este é um guia de como produzir documentação em Markdown. Para entender como criar documentos em Markdown no Github, veja o material/vídeo:
[Guia de Uso do Markdown](https://github.com/mc-unicamp/oficinas/tree/master/docs).

Vide detalhes sobre o Markdown em: [Mastering Markdown](https://guides.github.com/features/mastering-markdown/).

E mais especificamente sobre tabelas em: [Organizing information with tables](https://help.github.com/en/articles/organizing-information-with-tables)

Segue abaixo o modelo de como deve ser apresentado e documentado o projeto. Tudo o que for indicado entre `<...>` indica algo que deve ser substituído pelo indicado. No modelo são colocados exemplos ilustrativos, que serão substituídos pelos do seu projeto.

Segue abaixo o modelo de como devem ser documentadas as entregas.
> Tudo o que aparecer neste modo de citação se refere algo que deve ser substituído pelo indicado. No modelo são colocados exemplos ilustrativos, que serão substituídos pelos do seu projeto.


# Modelo para Apresentação do Projeto (Arquivo README.MD)

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
> Link para vídeo de apresentação da proposta do projeto (máximo 3 minutos).

# Perguntas de Pesquisa
> Perguntas de pesquisa que o projeto pretende responder ou hipóteses a serem avaliadas, enunciadas de maneira objetiva e verificável.

# Bases de Dados
> Elencar bases de dados candidatas a serem utilizadas no projeto.

# Metodologia
> Esta seção será evoluída ao longo do projeto. Nesta primeira entrega informe técnicas que pretende-se explorar
> tais como: aprendizagem de máquina, análise de redes, análise estatística, ou integração de uma ou mais técnicas. Para a primeira entrega, descreva de maneira mais genérica que tipo de abordagem seu grupo pretende realizar.

# Ferramentas
> Ferramentas a serem utilizadas (com base na visão atual do grupo sobre o projeto).

# Cronograma
> Proposta de cronograma. Procure estimar quantas semanas serão gastas para cada etapa do projeto.
