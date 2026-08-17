// # Glossary. Glossário.

#import "../packages.typ": quati-abnt.common.components.foreign_text

#let abbreviations_entries = (
  (
    key: "abnt",
    short: "ABNT",
    long: "Associação Brasileira de Normas Técnicas",
    group: "Normatização",
  ),
  (
    key: "nbr",
    short: "NBR",
    plural: "NBRs",
    long: "Norma Brasileira",
    longplural: "Normas Brasileiras",
    group: "Normatização",
  ),
  (
    key: "ml",
    short: "ML",
    long: "aprendizado de máquina",
    custom: foreign_text[machine learning],
    group: "Computação",
  ),
)

#let glossary_entries = (
  (
    key: "rn",
    short: "rede neural",
    plural: "redes neurais",
    custom: foreign_text[neural network],
    description: [Em inglês, #foreign_text[neural network]. Modelo computacional composto por camadas de unidades interligadas que aprendem padrões em dados por meio de ajustes de pesos @li:2022:survey_convolutional_neural_networks.],
    group: "Computação",
  ),
)

#let symbols_entries = ()


#let glossaries_entries = (
  ..abbreviations_entries,
  ..glossary_entries,
  ..symbols_entries,
)
