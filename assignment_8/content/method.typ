#import "../components.typ": *

= Materiais e método <seção:método>

#editor_note(prefixes: (
  (body: "Função da seção"),
))[Permitir que outro pesquisador reproduza o experimento, descrevendo preparação dos dados, análise exploratória, divisão treino/teste, balanceamento, modelos, ajuste de hiperparâmetros, métricas e protocolo de repetição.]

== Pré-processamento e análise exploratória

#done_note(
  prefixes: ((body: "Variáveis consideradas no modelo"),),
)[Informar que foram verificadas duplicatas e valores ausentes e registrar como esses aspectos foram tratados. Explicar a remoção/omissão de identificadores do conjunto de preditores e a definição da representação final.]

Não foram encontradas duplicatas na base, nem valores ausentes.
Algumas características dentais apresentaram nenhuma ou quase nenhuma contagem acima de 0.
Por esse motivos foram removidas:
`RiM`, `I`, `Ri`, `TeM` e `Cp`.

#done_note(prefixes: (
  (body: "Análise exploratória"),
))[Descrever a análise das distribuições de idade, faixas etárias, condição da boca e contagens de condições dentais. Explicar que a EDA foi usada para orientar a seleção de atributos e identificar assimetria, muitos valores nulos/zero, possíveis outliers e diferenças entre faixas etárias.]

As características `H` (dentes saudáveis) e `R` (restaurações) apresentaram uma quantidade suficiente de registros para fazer tratamento convencional de #get_term("outlier", plural: true) por #gls("iqr").
Contudo, as demais características numéricas apresentaram contagens muito próximas de 0.
Assim, decidimos não realizar alisamento de dados, e optar por métodos baseados em árvore.
Ainda, a característica `sexo` e `Dc` foram removidas por apresentarem distribuição muito parecida entre as faixas-etárias.

#done_note(prefixes: (
  (body: "Análise de associações"),
))[Documentar as associações entre variáveis numéricas por Spearman/Pearson, entre categóricas por Cramér's V e entre numéricas e categóricas por eta-quadrado/ANOVA. Explicar como essas análises apoiaram a seleção dos atributos, sem confundir associação com causalidade.]

Em seguida, as características foram sujeitas a análises de associação.
Entre as numéricas, foi usado o método de Spearman, mostrado na @figura:correlacao_de_spearman, e também de Pearson.
Ambas não detectaram correlações significativas.
Também foram realizados testes de associação por eta-quadrado e ANOVA, que igualmente não acusaram.
Por essa razão, todas as características foram usadas na validação e teste.
Como benefício nos métodos em árvore, ressalta-se a capacidade de atribuir maior importância às melhores características.

#figure(
  caption: [Correlação de Spearman],
)[
  #image("../assets/correlacao_de_spearman.png")
] <figura:correlacao_de_spearman>

== Divisão e validação

#done_note(prefixes: (
  (body: "Divisão dos dados"),
))[Registrar a separação estratificada em 80% para treino/validação (739 instâncias) e 20% para teste (185 instâncias), usando as sete faixas etárias para preservar a distribuição do alvo.]

Antes de iniciar o processamento, a base de dados foi dividida nas partições de validação e de teste, na proporção de 80% (739 instâncias) a 20% (185 instâncias).
A separação foi feita de forma estratificada pelas 7 faixas-etárias sob a #get_term("seed") 27.

#done_note(prefixes: (
  (body: "Reprodutibilidade"),
))[registrar sementes utilizadas (27, 32, 59, 74 e 93), bibliotecas/ambiente relevantes e as escolhas determinísticas necessárias para repetir os experimentos.]

Todos os procedimentos de validação foram realizados em cinco execuções, com as #get_term("seed", plural: true): 27, 32, 59, 74, e 93.
Além disso, cada execução usou validação cruzada com 5 #get_term("fold", plural: true).
O experimento foi implementado na linguagem Python 3.14, utilizando as bibliotecas `pandas` e `numpy` para manipulação de dados.
Foi feito balanceamento pelo `imbalanced-learn`, e os algoritmos de #get_term("md") foram disponibilizados pelo `scikit-learn`.

#done_note(prefixes: (
  (body: "Balanceamento"),
))[Explicar que SMOTE foi comparado a nenhuma aplicação de balanceamento apenas na tarefa de classificação. Descrever que a comparação foi feita por validação cruzada estratificada com cinco folds e cinco sementes fixas, totalizando 25 execuções por configuração. Especificar a posição do SMOTE no pipeline, para evitar vazamento de informação entre folds.]

Em seguida, avaliamos a necessidade de realizar balanceamento sintético na base.
Aplicamos validação cruzada sobre os algoritmos de classificação, variando o método de #gls("smote") ativo e desligado.
Os resultados foram comparados pela métrica #get_term("f1_macro"), como apresentado na @tabela:balanceamento.
Não se constatou diferença significativa entre os testes, de forma que ambas as opções foram levadas para a fase de validação.

#figure(
  caption: [Comparação de #get_term("f1_macro") com balanceamento],
)[
  #table(
    columns: (auto, auto),
    align: (start, end),
    table.header(strong[Modelo], strong[F1 macro]),
    [Árvore de decisão #text(fill: red)[sem] SMOTE], [0.337 ± 0.013],
    [Árvore de decisão #text(fill: blue)[com] SMOTE], strong[0.345 ± 0.009],
    table.hline(stroke: 0.25pt),
    [Floresta aleatória #text(fill: red)[sem] SMOTE], strong[0.370 ± 0.006],
    [Floresta aleatória #text(fill: blue)[com] SMOTE], [0.369 ± 0.013],
  )
] <tabela:balanceamento>

== Modelos e configuração experimental

#editor_note(prefixes: (
  (body: "Ajuste de hiperparâmetros"),
))[Documentar o GridSearch com validação cruzada estratificada em cinco folds por cinco sementes. Informar que F1 macro foi a métrica de seleção para classificação e MAE para regressão. Apresentar somente os espaços de busca e a configuração final no corpo do texto; deixar resultados completos do grid para material suplementar/apêndice, caso necessário.]

#editor_note(prefixes: (
  (body: "Avaliação final"),
))[Explicar que os modelos selecionados são avaliados no conjunto de teste separado, com cinco sementes fixas. Registrar que as tabelas apresentam média ± desvio padrão entre sementes.]

#editor_note(prefixes: (
  (body: "Métricas"),
))[Definir acurácia, acurácia balanceada e F1 macro para classificação; MAE, RMSE e R² para regressão. Justificar o uso de F1 macro e acurácia balanceada diante do desbalanceamento das faixas.]

== Métricas e protocolo de avaliação

#todo_note()[
  Definir as métricas utilizadas e explicar como as médias e desvios padrão foram calculados entre as cinco sementes no conjunto de teste.
]
