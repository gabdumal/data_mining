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
  == Multi-step ahead predictive model for blood glucose concentrations of type-1 diabetic patients#footnote[
    #cite(<zaidi:2021:glucose_regression>, form: "full")
  ]


  #stress[Objetivo:] prever os valores futuros da *glicemia* no sangue (BG) (em mg/dL), em múltiplos *instantes* à frente (multi-step forecasting).
  - Utiliza o histórico recente de glicemia, alimentação e administração de insulina de pacientes com *diabetes tipo 1*.

  #colbreak()
  #stress[Base de dados:] *300 pacientes* (filtrados para *97*) com diagnóstico de ao menos 2 anos e 18 de idade. Uso de séries temporais de medições de glicose contínuas.

  #stress[Variáveis de entrada]
  1. Histórico da glicemia (CGM)
  + Ingestão de carboidratos (Meal intake)
  + Taxa basal de insulina (Basal insulin)
  + Bolus de insulina (Bolus insulin)

  As observações são registradas a cada *5 minutos*.

  Outras informações existem na base, mas não são usadas, como: idade, sexo, anos desde o diagnóstico, atividade física, entre outras.

  #colbreak()
  #stress[Resultados]
  - O modelo apresentou boa *precisão* para previsões de até *30 minutos*.
    - Saída em valores *contínuos* de mg/dL.
    - RMSE de 23.22 ± 6.39 mg/dL.
  - Autores afirmam indicar *utilidade clínica*.
    - Aproximadamente 80% das previsões ficaram na Zona A da grade de Clarke.
    - Aproximadamente 85% ficaram na Zona A da grade de Parkes.

]

#title_slide("Agrupamento")
#slide[
  == Deep embedded clustering generalisability and adaptation for integrating mixed datatypes: two critical care cohorts#footnote[
    #cite(<kok:2024:icu_clustering>, form: "full")
  ]

  #stress[Objetivo:] identificar *grupos* de pacientes em *UTI* com características clínicas *semelhantes*, sem utilizar rótulos previamente definidos.

  #colbreak()
  #stress[Base de dados: ] o estudo comparou duas bases de dados: uma para o desenvolvimento e outra para validação.

  - *SICS:* coorte prospectiva do University Medical Center Groningen (Países Baixos) --- *787* internações.
  - *MUMC+:* base retrospectiva de *3.894* internações (filtradas de 6.328) admitidas no Maastricht University Medical Centre+ (Países Baixos) entre 09/07/2012 e 14/03/2020.

  #colbreak()
  #stress[Variáveis de entrada: ] foram elencadas *80* variáveis, representadas de forma *binária*. Destacam-se:
  - Idade
  - Sexo
  - Exames laboratoriais (23 medidas, representadas pela média e desvio padrão durante a internação)
  - Frequência cardíaca
  - Pressão arterial
  - Temperatura
  - Ventilação mecânica (definida constante quando não usada)
  - Pressão venosa central (medição invasiva ou por indicador)
  - Tipo de admissão

  #colbreak()
  #stress[Resultados]

  O modelo identificou *seis grupos* clinicamente distintos, semelhantes aos encontrados em estudos anteriores:
  1. Insuficiência renal
  + Trauma e neurologia
  + Choque cardiovascular e hemorragia
  + Doenças cardiovasculares e respiratórias crônicas
  + Infecção
  + Falência grave de múltiplos órgãos.

  Os agrupamentos também puderam ser *reproduzidos* na base de validação, indicando boa capacidade de generalização.

]

#title_slide("Regras de associação")
#slide[

  == Enhancing Retail Transactions: A Data-Driven Recommendation Using Modified RFM Analysis and Association Rules Mining#footnote[
    #cite(<chen:2023:retail_association_rules>, form: "full")
  ]


]
