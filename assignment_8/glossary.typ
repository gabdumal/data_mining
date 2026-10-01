// # Glossary. Glossário.

#import "packages.typ": quati-abnt.common.components.foreign_text

#let abbreviations_entries = (
  (
    key: "cbct",
    short: "CBCT",
    long: "tomografia computadorizada de feixe cônico",
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
