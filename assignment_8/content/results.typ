#import "../components.typ": *

= Resultados <seção:resultados>

#editor_note(prefixes: (
  body: "Função da seção",
))[apresentar evidências e interpretá-las em relação às perguntas do trabalho e à literatura, separando claramente resultados da EDA, resultados de validação e desempenho no teste.]

#editor_note(prefixes: (
  body: "Caracterização da base",
))[apresentar os principais padrões encontrados na EDA: distribuição de idade e faixas, distribuição da condição da boca, prevalência/concentração das condições dentais e presença de atributos esparsos ou com outliers. Não transformar a seção em um catálogo de todos os gráficos dos notebooks.]

#editor_note(prefixes: (
  body: "Seleção de atributos",
))[mostrar de forma resumida quais variáveis permaneceram e por quê. A heatmap de Spearman pode ser usada como evidência principal, acompanhada de uma interpretação cuidadosa das poucas associações mais relevantes.]

#editor_note(prefixes: (
  body: "Balanceamento",
))[apresentar a comparação com e sem SMOTE para Decision Tree e Random Forest. Relatar as diferenças observadas em F1 macro, acurácia balanceada e acurácia. Como os artefatos disponíveis não mostram um teste de hipótese, usar linguagem descritiva ("maior", "menor", "diferença observada"), evitando a expressão "diferença estatisticamente significativa".]

#editor_note(prefixes: (
  body: "Validação e hiperparâmetros",
))[apresentar uma tabela compacta com a configuração final de cada modelo e a métrica utilizada na seleção. O objetivo aqui é mostrar como cada configuração foi escolhida, sem despejar as centenas/milhares de combinações do GridSearch.]

#editor_note(prefixes: (
  body: "Desempenho de classificação",
))[comparar Decision Tree e Random Forest, com e sem SMOTE, no conjunto de teste. Apresentar acurácia, acurácia balanceada e F1 macro como média ± desvio padrão entre as cinco sementes. Explicar que uma configuração pode apresentar melhor desempenho em uma métrica e não em outra.]

#editor_note(prefixes: (
  body: "Desempenho de regressão",
))[apresentar MAE, RMSE e R² do Gradient Boost, também como média ± desvio padrão entre sementes. Interpretar os erros em anos e comentar o comportamento global da relação entre idade real e estimada.]

#editor_note(prefixes: (
  body: "Desempenho por faixa etária",
))[usar as métricas por classe e as matrizes de confusão para identificar as faixas nas quais os classificadores apresentam maior dificuldade. Relacionar os erros às diferentes quantidades de exemplos e à sobreposição entre faixas vizinhas, quando suportado pelos dados.]

#editor_note(prefixes: (
  body: "Resíduos da regressão",
))[analisar o gráfico real × estimado e a distribuição dos resíduos, observando tendência, dispersão e possíveis regiões de erro sistemático sem extrapolar além do que os gráficos permitem afirmar.]

#editor_note(prefixes: (
  body: "Importância das características",
))[discutir as importâncias produzidas pelos modelos. Destacar convergências e diferenças entre Decision Tree, Random Forest e Gradient Boost e relacioná-las com os padrões observados na EDA. Tratar importância de variável como medida específica do modelo, e não como evidência causal.]

#editor_note(prefixes: (
  body: "Comparação com literatura",
))[confrontar os resultados com trabalhos diretamente comparáveis, dando prioridade a estudos com população adulta, dados odontológicos semelhantes e métricas compatíveis. Quando não houver comparação direta, declarar a diferença de cenário em vez de forçar uma comparação numérica.]

#editor_note(prefixes: (
  body: "Limitações observadas nos resultados",
))[antecipar a discussão de baixa representação em algumas faixas, dependência da base local, agregação das anotações e possíveis perdas de informação estrutural ou espacial.]

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
  - Decision Tree sem SMOTE: acurácia 0.4076 ± 0.0048; acurácia balanceada 0.3751 ± 0.0034; F1 macro 0.3607 ± 0.0037.
  - Decision Tree com SMOTE: acurácia 0.4130 ± 0.0197; acurácia balanceada 0.4233 ± 0.0163; F1 macro 0.3703 ± 0.0100.
  - Random Forest sem SMOTE: acurácia 0.4443 ± 0.0089; acurácia balanceada 0.3859 ± 0.0092; F1 macro 0.3959 ± 0.0102.
  - Random Forest com SMOTE: acurácia 0.4400 ± 0.0141; acurácia balanceada 0.4181 ± 0.0170; F1 macro 0.4166 ± 0.0147.
  - Gradient Boost: MAE 7.0471 ± 0.0058; RMSE 9.3780 ± 0.0042; R² 0.7152 ± 0.0003.

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
