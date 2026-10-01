#import "../components.typ": *

= Resultados <seção:resultados>

#editor_note(prefixes: (
  (body: "Função da seção"),
))[Apresentar evidências e interpretá-las em relação às perguntas do trabalho e à literatura, separando claramente resultados da EDA, resultados de validação e desempenho no teste.]


#done_note(prefixes: (
  (body: "Desempenho de classificação"),
))[Comparar Decision Tree e Random Forest, com e sem SMOTE, no conjunto de teste. Apresentar acurácia, acurácia balanceada e F1 macro como média ± desvio padrão.]

A @tabela:teste_classificação apresenta os resultados da fase de teste para os modelos de classificação.
A métrica de maior relevância é o #get_term("f1_macro"), com 0,4116 ± 0,0152 para a #gls("rf") com #gls("smote"), que também teve a melhor acurácia balanceada.
O mesmo algoritmo teve a melhor #get_term("accuracy") na versão sem balanceamento, o que justifica a decisão de realizar a fase de teste com e sem #gls("smote").
Quanto à #gls("dt"), ela apresentou resultados consistentemente menos vantajosos.

#figure(
  caption: [Resultados dos testes dos métodos de classificação],
)[
  #table(
    columns: (3cm, 1.75cm, 1.75cm, 1.75cm),
    table.header(strong[Modelo], strong[Acurácia], strong[Acc. balanceada], strong[F1 macro]),

    [Árvore de decisão\ #text(fill: red)[sem] balanceamento],
    [0,3978\ ± 0,0030],
    [0,3669\ ± 0,0020],
    [0,3531\ ± 0,0021],

    [Árvore de decisão\ #text(fill: blue)[com] balanceamento],
    [0,4141\ ± 0,0277],
    [0,3981\ ± 0,0318],
    [0,3847\ ± 0,0333],

    [Floresta aleatória\ #text(fill: red)[sem] balanceamento],
    strong[0,4497\ ± 0,0080],
    [0,3860\ ± 0,0089],
    [0,3913\ ± 0,0097],

    [Floresta aleatória\ #text(fill: blue)[com] balanceamento],
    [0,4292\ ± 0,0156],
    strong[0,4125\ ± 0,0144],
    strong[0,4116\ ± 0,0152],
  )
] <tabela:teste_classificação>

Os resultados se mostraram pouco satisfatórios a princípio, o que exige a análise dos erros por classe-alvo de forma a identificar a dificuldade dos modelos.
A matriz de confusão da #gls("dt") sem #gls("smote") na @figura:matriz_de_confusao_de_decision_tree_sem_smote.png apresentou um acerto maior que 40% nas classes de 20 a 49 anos, enquanto a faixa de 60--69 acertou apenas 8,7%, e teve desempenho baixo no geral nas mais avançadas.
Sua versão balanceada, na @figura:matriz_de_confusao_de_decision_tree_com_smote.png, melhorou o acerto nas duas primeiras faixas etárias e nas três últimas, enquanto a redução das medianas foi insignificante.\

#figure(
  caption: [Matriz de confusão da árvore de decisão sem SMOTE],
)[
  #image("../assets/matriz_de_confusao_de_decision_tree_sem_smote.png")
] <figura:matriz_de_confusao_de_decision_tree_sem_smote.png>

#figure(
  caption: [Matriz de confusão da árvore de decisão com SMOTE],
)[
  #image("../assets/matriz_de_confusao_de_decision_tree_com_smote.png")
] <figura:matriz_de_confusao_de_decision_tree_com_smote.png>

Em relação à #gls("rf") sem #gls("smote") (@figura:matriz_de_confusao_de_random_forest_sem_smote.png), o acerto bom da classe 20--29 foi acentuado para 87,5%.
Entretanto, as classes abaixo e acima dessa tenderam a classificar dentro dela os registros.
Gravemente, a classe 30--39 perdeu quase toda a capacidade de predição, que também vazou para a classe posterior.
A dificuldade das duas classe mais idosas se manteve.
Finalmente, sua versão balanceada (@figura:matriz_de_confusao_de_random_forest_com_smote.png) apresentou a melhor diagonal, tendo sua maior dificuldade na classe 50--59, enquanto destaca o acerto das mais jovens, e equilibra as demais.

#figure(
  caption: [Matriz de confusão da floresta aleatória sem SMOTE],
)[
  #image("../assets/matriz_de_confusao_de_random_forest_sem_smote.png")
] <figura:matriz_de_confusao_de_random_forest_sem_smote.png>

#figure(
  caption: [Matriz de confusão da floresta aleatória com SMOTE],
)[
  #image("../assets/matriz_de_confusao_de_random_forest_com_smote.png")
] <figura:matriz_de_confusao_de_random_forest_com_smote.png>








#editor_note(prefixes: (
  (body: "Desempenho de regressão"),
))[Apresentar MAE, RMSE e R² do Gradient Boost, também como média ± desvio padrão entre sementes. Interpretar os erros em anos e comentar o comportamento global da relação entre idade real e estimada.]

#editor_note(prefixes: (
  (body: "Desempenho por faixa etária"),
))[Usar as métricas por classe e as matrizes de confusão para identificar as faixas nas quais os classificadores apresentam maior dificuldade. Relacionar os erros às diferentes quantidades de exemplos e à sobreposição entre faixas vizinhas, quando suportado pelos dados.]

#editor_note(prefixes: (
  (body: "Resíduos da regressão"),
))[Analisar o gráfico real × estimado e a distribuição dos resíduos, observando tendência, dispersão e possíveis regiões de erro sistemático sem extrapolar além do que os gráficos permitem afirmar.]

#editor_note(prefixes: (
  (body: "Importância das características"),
))[Discutir as importâncias produzidas pelos modelos. Destacar convergências e diferenças entre Decision Tree, Random Forest e Gradient Boost e relacioná-las com os padrões observados na EDA. Tratar importância de variável como medida específica do modelo, e não como evidência causal.]

#editor_note(prefixes: (
  (body: "Comparação com literatura"),
))[Confrontar os resultados com trabalhos diretamente comparáveis, dando prioridade a estudos com população adulta, dados odontológicos semelhantes e métricas compatíveis. Quando não houver comparação direta, declarar a diferença de cenário em vez de forçar uma comparação numérica.]

#editor_note(prefixes: (
  (body: "Limitações observadas nos resultados"),
))[Antecipar a discussão de baixa representação em algumas faixas, dependência da base local, agregação das anotações e possíveis perdas de informação estrutural ou espacial.]

== Caracterização da base e análise exploratória
#todo_note(
  prefixes: ((body: "Figuras recomendadas"),),
)[
  + distribuição da idade/faixas etárias;
  + condição da boca por faixa etária;
  + um ou dois exemplos representativos das distribuições das condições dentais, priorizando variáveis informativas e/ou com outliers.

  A maior parte dos gráficos adicionais dos notebooks deve ficar fora do corpo principal ou ser omitida. O texto deve responder: quais padrões da base justificam as etapas seguintes?
]

== Seleção de características e associações
#todo_note()[
  Incluir a heatmap de Spearman e, apenas se realmente ajudar, uma pequena tabela com as associações mais fortes. Explicar que as análises serviram como apoio à seleção, e não como prova de que uma variável individual determina a idade.
]

== Balanceamento e validação
#todo_note()[
  Incluir uma tabela resumida do experimento com/sem SMOTE e outra tabela com os hiperparâmetros selecionados. Os resultados completos do GridSearch por seed podem ser relegados ao apêndice.
]

== Desempenho no teste
#todo_note()[
  Incluir uma tabela principal com as três métricas de classificação para os quatro modelos/configurações de classificação e uma tabela separada com MAE, RMSE e R² para o Gradient Boost.

  Registrar os valores consolidados encontrados nos artefatos de teste:
  - Decision Tree sem SMOTE: acurácia 0,4076 ± 0,0048; acurácia balanceada 0,3751 ± 0,0034; F1 macro 0,3607 ± 0,0037.
  - Decision Tree com SMOTE: acurácia 0,4130 ± 0,0197; acurácia balanceada 0,4233 ± 0,0163; F1 macro 0,3703 ± 0,0100,
  - Random Forest sem SMOTE: acurácia 0,4443 ± 0,0089; acurácia balanceada 0,3859 ± 0,0092; F1 macro 0,3959 ± 0,0102.
  - Random Forest com SMOTE: acurácia 0,4400 ± 0,0141; acurácia balanceada 0,4181 ± 0,0170; F1 macro 0,4166 ± 0,0147.
  - Gradient Boost: MAE 7.0471 ± 0,0058; RMSE 9.3780 ± 0,0042; R² 0,7152 ± 0,0003.

  Interpretar esses números sem reduzir a análise a uma classificação única de "melhor modelo": discutir o comportamento por métrica e por tarefa.
]

== Erros por faixa etária e análise de resíduos
#todo_note()[
  Usar matrizes de confusão, métricas por faixa e o gráfico de idade real × estimada. Priorizar os padrões que alteram a interpretação dos resultados: classes com maior dificuldade, dispersão entre sementes e possíveis vieses de subestimação/superestimação.
]

== Importância das características
#todo_note()[
  Consolidar as cinco análises de importância em uma figura/tabela legível, evitando as cinco pizzas pequenas lado a lado no texto principal. Destacar as características com maior contribuição segundo cada algoritmo e discutir consistência entre modelos.
]

== Comparação com trabalhos relacionados
#todo_note()[
  Construir uma comparação textual e, se houver dados realmente compatíveis, uma tabela com: trabalho, base/população, entrada, tarefa, método e métrica. Explicitar qualquer diferença de protocolo que impeça uma comparação direta dos números.
]
