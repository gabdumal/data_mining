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
A matriz de confusão da #gls("dt") sem #gls("smote") na @figura:matriz_de_confusao_de_decision_tree_sem_smote apresentou um acerto maior que 40% nas classes de 20 a 49 anos, enquanto a faixa de 60--69 acertou apenas 8,7%, e teve desempenho baixo no geral nas mais avançadas.
Sua versão balanceada, na @figura:matriz_de_confusao_de_decision_tree_com_smote, melhorou o acerto nas duas primeiras faixas etárias e nas três últimas, enquanto a redução das medianas foi insignificante.\

#figure(
  caption: [Matriz de confusão da árvore de decisão sem SMOTE],
)[
  #image("../assets/matriz_de_confusao_de_decision_tree_sem_smote.png")
] <figura:matriz_de_confusao_de_decision_tree_sem_smote>

#figure(
  caption: [Matriz de confusão da árvore de decisão com SMOTE],
)[
  #image("../assets/matriz_de_confusao_de_decision_tree_com_smote.png")
] <figura:matriz_de_confusao_de_decision_tree_com_smote>

Em relação à #gls("rf") sem #gls("smote") (@figura:matriz_de_confusao_de_random_forest_sem_smote), o acerto bom da classe 20--29 foi acentuado para 87,5%.
Entretanto, as classes abaixo e acima dessa tenderam a classificar dentro dela os registros.
Gravemente, a classe 30--39 perdeu quase toda a capacidade de predição, que também vazou para a classe posterior.
A dificuldade das duas classe mais idosas se manteve.
Finalmente, sua versão balanceada (@figura:matriz_de_confusao_de_random_forest_com_smote) apresentou a melhor diagonal, tendo sua maior dificuldade na classe 50--59, enquanto destaca o acerto das mais jovens, e equilibra as demais.

#figure(
  caption: [Matriz de confusão da floresta aleatória sem SMOTE],
)[
  #image("../assets/matriz_de_confusao_de_random_forest_sem_smote.png")
] <figura:matriz_de_confusao_de_random_forest_sem_smote>

#figure(
  caption: [Matriz de confusão da floresta aleatória com SMOTE],
)[
  #image("../assets/matriz_de_confusao_de_random_forest_com_smote.png")
] <figura:matriz_de_confusao_de_random_forest_com_smote>

#done_note(prefixes: (
  (body: "Desempenho de regressão"),
))[Apresentar MAE, RMSE e R² do Gradient Boost, também como média ± desvio padrão entre sementes. Interpretar os erros em anos e comentar o comportamento global da relação entre idade real e estimada.]

A regressão apresentou resultado bem mais interessante, com erro médio absoluto de 7.1895 ± 0.0048 anos, o que se aproxima do 5,89 anos da literatura, mesmo utilizando uma fonte de dados menos precisa.
A @tabela:teste_regressão também apresenta o RMSE e R², que acompanham o resultado satisfatório, ainda que passível de melhorias.

#figure(
  caption: [Resultados dos testes do #foreign_text[Gradient Boost]],
)[
  #table(
    columns: (3cm, 1.75cm, 1.75cm, 1.75cm),
    table.header(strong[Modelo], strong[MAE], strong[RMSE], strong[R²]),

    [Gradient Boost], [7.1895\ ± 0.0048], [9.6785\ ± 0.0010], [0.6967\ ± 0.0001],
  )
] <tabela:teste_regressão>

Apesar de o #gls("gb") ter sido aplicada como modelo de regressão, categorizamos as predições numéricas nas mesmas faixas-etárias utilizadas na classificação.
A diagonal da sua matriz de confusão na @figura:matriz_de_confusao_de_gradient_boost foi a mais demarcada do experimento, resolvendo o problema da classe 60--69, enquanto manteve a qualidade das duas mais jovens.
Contudo, destaca-se a dificuldade nas classes 30--39 e 50--59.
Mais importante: a classe 70+ foi totalmente ignorada pelo modelo, que levou a maior parte de suas predições para a anterior.
O #foreign_text[scatterplot] do #gls("gb") (@figura:scatterplot_de_gradient_boost) acentua o acerto do modelo nas classes mais jovens e mais idosas, com a exceção da 70+.

#figure(
  caption: [Matriz de confusão do Gradient Boost],
)[
  #image("../assets/matriz_de_confusao_de_gradient_boost.png")
] <figura:matriz_de_confusao_de_gradient_boost>

#figure(
  caption: [#foreign_text[Scatterplot] do Gradient Boost],
)[
  #image("../assets/scatterplot_de_gradient_boost.png")
] <figura:scatterplot_de_gradient_boost>

#done_note(prefixes: (
  (body: "Importância das características"),
))[Discutir as importâncias produzidas pelos modelos. Destacar convergências e diferenças entre Decision Tree, Random Forest e Gradient Boost e relacioná-las com os padrões observados na EDA.]

A @figura:importancia_das_caracteristicas demostra a importância de cada característica para os modelos testados.
A quantidade de dentes saudáveis (`H`) e de restaurações (`R`), que estão melhor representadas em dados, são consistentemente as mais importantes.
Os rótulos de qualidade geral da boca foram pouco utilizados, chegando a importância 0, o que pode significar que suas conclusões são bem estimadas por combinações de características numéricas.
Ressalta-se também a menor distribuição de importâncias no #gls("gb"), que teve 0.690 na `H`.

#figure(
  caption: [Importância das características],
)[
  #image("../assets/importancia_das_caracteristicas.png")
] <figura:importancia_das_caracteristicas>

A @figura:barras_de_real_vs_estimado demostra o desempenho de acerto dos modelos em relação à distribuição real
Para as classes de 10--19, 30--39, 40--49 e 50--59 a #gls("dt") sem #gls("smote") acompanhou da melhor forma a representação original, o que se mostra curioso, dado que apresentou o menor #get_term("f1_macro").
Isso ocorre devido ao seu grande erro nas demais classes, sobretudo a 60--69.
Para a classe de 20--29 anos, o melhor modelo foi o #gls("gb"), mesmo que ele tenha classificado bem mais registros nessa classe do que realmente existem.
Já na classe 60--69, a #gls("rf") com balanceamento demonstrou os melhores resultados às custas de desempenho pior na anterior.
Finalmente, a classe 70+ é melhor modelada pelo #gls("rf") sem #gls("smote").
Em geral, o #gls("gb") apresentou uma distribuição aceitável.

#figure(
  caption: [Gráfico de barras da quantidade de registros classificados em cada faixa-etária em relação à representação real],
)[
  #image("../assets/barras_de_real_vs_estimado.png")
] <figura:barras_de_real_vs_estimado>
