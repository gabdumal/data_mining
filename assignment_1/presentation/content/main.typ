#import "../packages.typ": *
#import "../components.typ": *
#import "../template.typ": *


#title_slide("Classificação")
#slide[
  == Age group prediction with panoramic radiomorphometric parameters using machine learning algorithms#footnote[
    #cite(<lee:2022:age_group_classification>, form: "full")
  ]

  #stress[Objetivo:] relacionar 18 *parâmetros* rádio-morfométricos extraídos de *radiografias* panorâmicas odontológicas com *faixas etárias* pré-determinadas.

  #stress[Base de dados:] *471* pacientes (*209* homens e *262* mulheres) entre *10 e 69 anos* que visitaram o Hospital Odontológico Universitário de Kyung Hee, na Coreia do Sul entre 1 de abril de 2017 e 31 de março de 2020.

  #colbreak()
  #stress[Parâmetros]
  1. Distância entre o canal mandibular e a crista alveolar
  + Área do dente do primeiro molar superior
  + Área da polpa do primeiro molar superior
  + Área do dente do primeiro molar inferior
  + Área da polpa do primeiro molar inferior
  + Comprimento da raiz do canino superior
  + Número total de dentes
  + Número de tratamentos endodônticos na arcada inferior
  + Número de tratamentos endodônticos na arcada superior
  + Comprimento da coroa do canino superior

    #colbreak()
  #stress[Parâmetros]
  11. Distância entre o ápice da raiz do primeiro molar e o nervo alveolar inferior
  + Distância entre o forame mentual e a borda inferior da mandíbula
  + Distância entre o forame mentual e a crista alveolar
  + Número de coroas dentárias na arcada superior
  + Número de coroas dentárias na arcada inferior
  + Número de implantes na arcada superior
  + Número de implantes na arcada inferior
  + Presença de periodontite

    #colbreak()
    #stress[Grupos]
    #table(
      columns: 2,
      column-gutter: 1em,
      inset: 0.5em,

      table.header([*Primeira divisão*], [*Segunda divisão*]),

      table.cell(rowspan: 2)[Jovem: 10 a 19 anos], [10 a 19 anos], [20 a 29 anos],
      table.cell(rowspan: 2)[Adulto: 20 a 49 anos], [30 a 39 anos], [40 a 49 anos],
      table.cell(rowspan: 2)[Idoso: 50 a 69 anos], [50 a 59 anos], [60 a 69 anos],
    )

    #colbreak()
    #stress[Resultados]
    - Determinados *parâmetros* se mostraram mais efetivos para classificar um paciente no grupo de *jovens* do que nos outros,
      - como a área de polpa;
    - o mesmo ocorreu em relação a demais parâmetros para os grupos mais *idosos*,
      - como a quantidade de dentes e de implantes.
    - A predição demonstrou *melhor desempenho* para os grupos nos *extremos de idade* do que para o de adultos.

]

#title_slide("Regressão")
#slide[
  == Multi-step ahead predictive model for blood glucose concentrations of type-1 diabetic patients

  Texto #cite_prose(<zaidi:2021:glucose_regression>)#footnote[
    #cite(<zaidi:2021:glucose_regression>, form: "full")
  ]

]

#title_slide("Agrupamento")
#slide[
  == Deep embedded clustering generalisability and adaptation for integrating mixed datatypes: two critical care cohorts

  Texto #cite_prose(<kok:2024:icu_clustering>)#footnote[
    #cite(<kok:2024:icu_clustering>, form: "full")
  ]

]

#title_slide("Regras de associação")
#slide[

  == Enhancing Retail Transactions: A Data-Driven Recommendation Using Modified RFM Analysis and Association Rules Mining

  Texto #cite_prose(<chen:2023:retail_association_rules>)#footnote[
    #cite(<chen:2023:retail_association_rules>, form: "full")
  ]

]
