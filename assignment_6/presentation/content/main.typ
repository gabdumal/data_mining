#import "../packages.typ": *
#import "../components.typ": *
#import "../template.typ": *


#focus_slide(
  color: navy,
  "Predição da idade de humanos com base em características odontológicas",
)

#title_slide("Problema")

== Cenário

A estimação da #stress[idade] com base dos *dentes* é comum nas áreas de investigação *forense*, de identificação de pessoas, e de planejamento para tratamento odontológico.
#footnote[
  #cite(<lee:2026:machine_learning_adult_age_estimation>, form: "full")
]

As mudanças #stress[características] de idade são mais perceptíveis em populações pediátricas do que em *adultos*, o que dificulta a exatidão da estimativa aferida por técnicos humanos.

#pagebreak()

== Técnicas

Em adultos, #stress[características] de interesse incluem:
- quantidade de dentes presentes e de implantes;
- nível de *desgaste* e restaurações;
- *proporção* da área entre a coroa do dente e a polpa#footnote[
    #cite(<pereira:2025:incisor_pulp_chamber_dataset>, form: "full")
  ].

Métodos #stress[estatísticos] convencionais requerem trabalho de aferência do *técnico* odontológico, e levam a distorções.

== Objetivo

Empregar métodos de #stress[@ml] para predizer a *idade* de humanos, com foco em *adultos*.

Utilizar #stress[entradas] de *dados* que requeiram *menor intervenção* e interpretação de técnicos odontológicos.

Realizar as manipulações de formas não invasivas, e que permitam *preservar* os dentes.
