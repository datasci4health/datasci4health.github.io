# E3 - Entrega Final - 2023.1 Ciência e Visualização de Dados em Saúde

O objetivo geral do projeto final desta disciplina é realizar a análise de dados relacionados à saúde, para usá-los em uma das seguintes possíveis tarefas: recomendação, estudo de associações, validação de hipóteses, análise exploratória, análise visual, análise comparativa e predição.

## Entrega Final

A entrega final do projeto consiste em duas etapas:
* Apresentação do Projeto a ser realizada em sala de aula nos dias 27/06 e 29/06/2023, em ordem de apresentação a ser comunicada no ambiente Classroom da disciplina. A apresentação valerá 2,0 pontos da nota final do projeto. 
* Atualização do repositório GitHub já criado anteriormente. A versão final do repositório será avaliada, valendo 6,0 pontos da nota final do projeto.

De maneira análoga às entregas E1 e E2, a atualização do repositório GitHub inclui:
* Atualização do arquivo README.md do projeto incluindo as seções do template abaixo.
* Após a finalização da edição do conteúdo da segunda entrega, atribuição da tag de release **2023.1_datasci4health_E3** no repositório de origem.
* **Pull request**  do projeto no  **branch  principal** até a data de entrega.

(As entregas E1 e E2 serão avaliadas conjuntamente e valerão 2,0 pontos da nota final do projeto.)


## Datas Importantes

* 25/06 - Data limite para pull request do repositório do projeto (será considerada a última versão até essa data e horário).
* 27/06 (Terça) - Apresentação de grupos - Parte 1. A partir das 16:00 
* 29/06 (Quinta) - Apresentação de grupos - Parte 2. A partir das 16:00 
(Presença obrigatória de todos os membros do grupo na data de apresentação. Requerida presença de todos os alunos da disciplina nas datas das apresentações). 
* 30/06 - Entrega da avaliação por pares (vide outras informações abaixo).

## Instruções para a Apresentação

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

A avaliação do projeto final será realizada não apenas pelos professores da disciplina, mas também passará por etapa de avaliação por pares. Instruções serão fornecidas posteriormente no ambiente Classroom da Disciplina.

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

Sempre que possível e permitido, é importante que sejam colocados apontadores para os dados originais para garantir a reprodutibilidade do processo. As bases originais devem ser colocadas na subpasta `raw`. Dados intermediários, tais como dados tratados, resumidos, etc. devem ser armazenados na pasta `interim`. Finalmente, coloque os dados finais que serviram de entrada para as suas análises na subpasta `processed`. Caso exista alguma limitação de armazenamento da base no Github, forneça links públicos para acesso aos dados.

## `notebooks`

Código do seu projeto que pode ser executado online sem instalação de software, tal como um notebook em Jupyter ou equivalente.

## `src`

Código em alguma linguagem ou projeto em Orange, Weka e similares.

Se for código em linguagem de programação, tente organizá-lo de forma que seja simples a sua execução por terceiros, por exemplo, acrescente as bibliotecas necessárias etc. Acrescente na raiz um arquivo `README.md` com as instruções básicas de instalação e execução.

## `assets`

Qualquer mídia usada no seu projeto: vídeo, ilustrações, arquivos PDF etc.

Note que nem todos os diretórios ou arquivos serão necessários para todos os projetos. Foque em seguir o padrão para os diretórios que forem necessários. Não crie diretórios que não serão utilizados.

Seu repositório deverá obrigatoriamente conter o arquivo README.md, arquivo de documentação Markdown, que deverá conter a descrição do projeto conforme orientações a seguir.


# Orientações Gerais para a Entrega Final


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

## Slides da Apresentação Final
> Link para slides da apresentação final do projeto.

# Introdução e Referenciais de Teóricos
> Contextualização do projeto
>
> Caracterização do problema
>
> Motivação
>
> Relevância
>
> Trabalhos relacionados
>
> Indicação (bastante resumida) da análise proposta
>
> Indicação (bastante resumida) dos resultados alcançados


# Perguntas de Pesquisa e Objetivos
> Perguntas de pesquisa (revisadas e atualizadas) que o projeto pretende responder ou hipóteses a serem avaliadas, enunciadas de maneira objetiva e verificável.
> Se a análise exploratória contribuiu para as perguntas de pesquisa, apresente aqui elementos de análise exploratória que ajudem a responder a questão.
> Objetivos principais e específicos

# Metodologia
> Abordagem adotada pelo projeto na busca pela resposta às perguntas de pesquisa.
> Justificar teoricamente, sempre que possível, a metodologia adotada.

## Bases de Dados e Evolução
> Elencar bases de dados estudadas e/ou utilizadas no projeto, organizando em duas partes. Primeiro aquelas que foram estudadas, mas não foram usadas e em seguida as bases adotadas.

### Bases Estudadas mas Não Adotadas

> Para cada base, coloque uma mini-tabela no modelo a seguir e depois detalhamento sobre como ela foi analisada/usada, conforme exemplo a seguir.

Base de Dados | Endereço na Web | Resumo descritivo
----- | ----- | -----
Título da Base | http://base1.org/ | Breve resumo (duas ou três linhas) sobre a base.

> Faça uma descrição sobre o que concluiu sobre esta base. Sugere-se que respondam perguntas ou forneçam informações indicadas a seguir:
> * O que descobriu sobre esse banco?
> * Quais as transformações e tratamentos (e.g., dados faltantes e limpeza) feitos?
> * Por que este banco não foi adotado?

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
>
> Resultados de Análise Exploratória
> * use estatística descritiva e gráficos;
> * inclua gráficos de sobre a distribuição dos dados (e.g., histogramas e boxplots);
> * analise correlação e use gráficos de dispersão;
> * descreva os resultados/gráficos, os analise e contextualize com o tema definido.

# Análises Realizadas
> Descrição detalhada das análises realizadas.
>
>Relate aqui também a evolução do projeto: possíveis problemas enfrentados e possíveis mudanças de trajetória. Relatar o processo para se alcançar os resultados é tão importante quanto os resultados.
>
> Nesta seção ou na seção de Resultados podem aparecer destaques de código como indicado a seguir. Note que foi usada uma técnica de highlight de código, que envolve colocar o nome da linguagem na abertura de um trecho com `~~~`, tal como `~~~python`.
>
> Os destaques de código devem ser trechos pequenos de poucas linhas, que estejam diretamente ligados a alguma explicação. Não utilize trechos extensos de código. Se algum código funcionar online (tal como um Jupyter Notebook), aqui pode haver links. No caso do Jupyter, preferencialmente para o Binder abrindo diretamente o notebook em questão.

~~~python
df = pd.read_excel("/content/drive/My Drive/Colab Notebooks/dataset.xlsx");
sns.set(color_codes=True);
sns.distplot(df.Hemoglobin);
plt.show();
~~~

## Ferramentas
> Panorama das ferramentas utilizadas incluindo discussão sobre o uso das mesmas

# Resultados
> Descrição dos resultados mais importantes obtidos.
>
> Apresente os resultados da forma mais rica possível, com gráficos e tabelas. Mesmo que o seu código rode online em um notebook, copie para esta parte a figura estática. A referência a código e links para execução online pode ser feita aqui ou na seção de Análises Realizadas (o que for mais pertinente).

# Discussão
> Discussão dos resultados. Relacionar os resultados com as perguntas de pesquisa ou hipóteses avaliadas.
>
> A discussão dos resultados também pode ser feita opcionalmente na seção de Resultados, na medida em que os resultados são apresentados. Aspectos importantes a serem discutidos: É possível tirar conclusões dos resultados? Quais? Há indicações de direções para estudo? São necessários trabalhos mais profundos?

# Conclusão
> Destacar as principais conclusões obtidas no desenvolvimento do projeto.
>
> Destacar os principais desafios enfrentados.
>
> Principais lições aprendidas.

# Trabalhos Futuros
> O que poderia ser melhorado se houvesse mais tempo?

# Referências Bibliográficas
> Lista de artigos, links e referências bibliográficas.
>
> Fiquem à vontade para escolher o padrão de referenciamento preferido pelo grupo.
