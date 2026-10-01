// # Glossary. Glossário.

#import "packages.typ": quati-abnt.common.components.foreign_text

#let abbreviations_entries = (
  (
    key: "cbct",
    short: "CBCT",
    plural: "CBCTs",
    long: "tomografia computadorizada de feixe cônico",
    longplural: "tomografias computadorizadas de feixe cônico",
    description: [em inglês, #foreign_text[cone beam computed tomography].],
  ),
  (
    key: "inredd",
    short: "InReDD",
    long: "Grupo de Pesquisa Interdisciplinar em Odontologia Digital",
    description: [em inglês, #foreign_text[Interdisciplinary Research Group in Digital Dentistry]],
  ),
  (
    key: "usp",
    short: "USP",
    long: "Universidade de São Paulo",
  ),
  (
    key: "dt",
    short: "DT",
    long: "árvore de decisão",
    description: [em inglês, #foreign_text[decision tree].],
  ),
  (
    key: "rf",
    short: "RF",
    long: "floresta aleatória",
    description: [em inglês, #foreign_text[random forest].],
  ),
  (
    key: "gb",
    short: "GB",
    long: foreign_text[gradient boosting],
  ),
  (
    key: "xgb",
    short: "XGB",
    long: "XGBoost",
    description: [Implementação de #foreign_text[gradient boosting].],
  ),
  (
    key: "smote",
    short: "SMOTE",
    long: foreign_text[Synthetic Minority Over-sampling Technique],
    description: [técnica estatística de aumento de dados para corrigir conjuntos desbalanceados.],
  ),
  (
    key: "ia",
    short: "IA",
    long: "inteligência artificial",
  ),
  (
    key: "fdi",
    short: "FDI",
    long: "Federação Dentária Internacional",
    description: [em inglês, #foreign_text[World Dental Federation].],
  ),
  (
    key: "lda",
    short: "LDA",
    long: foreign_text[linear discriminant analysis],
  ),
  (
    key: "lr",
    short: "LR",
    long: "regressão logística",
    description: [em inglês, #foreign_text[logistic regression].],
  ),
  (
    key: "svm",
    short: "SVM",
    long: "máquina de vetores de suporte",
    description: [em inglês, #foreign_text[Support Vector Machine].],
  ),
  (
    key: "mlp",
    short: "MLP",
    long: foreign_text[multilayer perceptron],
  ),
  (
    key: "nn",
    short: "NN",
    long: "redes neurais",
    description: [em inglês, #foreign_text[neural networks].],
  ),
  (
    key: "iqr",
    short: "IQR",
    long: "intervalo interquartil",
    description: [em inglês, #foreign_text[interquartile range].],
  ),
  (
    key: "mae",
    short: "MAE",
    long: "erro médio absoluto",
    description: [em inglês, #foreign_text[mean absolute error].],
  ),
  (
    key: "rmse",
    short: "RMSE",
    long: "raiz do erro quadrático médio",
    description: [em inglês, #foreign_text[root mean square error].],
  ),
  (
    key: "r2",
    short: [R#upper[2]],
    long: "coeficiente de determinação",
  ),
)

#let glossary_entries = (
  (
    key: "ml",
    sort: "aprendizado de máquina",
    short: "aprendizado de máquina",
    description: [em inglês, #foreign_text[machine learning].],
  ),
)

#let symbols_entries = ()


#let glossaries_entries = (
  ..abbreviations_entries,
  ..glossary_entries,
  ..symbols_entries,
)
