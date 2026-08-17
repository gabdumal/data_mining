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

As mudanças #stress[características] de idade são mais perceptíveis em crianças e jovens do que em *adultos*, o que dificulta a exatidão da estimativa aferida por técnicos humanos.

#pagebreak()

== Técnicas

Em adultos, #stress[características] de interesse incluem:
- quantidade de dentes presentes e de implantes;
- nível de *desgaste* e restaurações;
- *proporção* da área entre a coroa do dente e a polpa#footnote[
    #cite(<pereira:2025:incisor_pulp_chamber_dataset>, form: "full")
  ].

Métodos #stress[estatísticos] convencionais requerem trabalho de aferência do *técnico* odontológico, e levam a distorções.

#pagebreak()

== Objetivo

Empregar métodos de #stress[#glossarium.gls("ml", link: false)] para predizer a *idade* de humanos, com foco em *adultos*.

Utilizar #stress[entradas] de *dados* que requeiram *menor intervenção* e interpretação de técnicos odontológicos.

Realizar as manipulações de formas não invasivas, e que permitam *preservar* os dentes.


#title_slide("Abordagem")

== Métodos

O problema pode ser tratado como:
\
\

#stress[Classificação] em grupos etários\
#align(center)[
  #set text(fill: black.lighten(30%))
  [criança (01-14), jovem (15-25), adulto (26-99)]\ [0-20, 21-40, 41-60, 61-80, 81-100]
]

#stress[Regressão] da idade estimada
#align(center)[
  #set text(fill: black.lighten(30%))
  12.0, 27.8, 73.1, ...
]

#pagebreak()

#grid(
  align: (top, horizon),
  columns: (1fr, auto),
  rows: 1fr,
  gutter: 16pt,

  [
    == Entrada

    #stress[#glossarium.gls("cbct", capitalize: true, link: false)]

    - Visualiza todos os ângulos.
    - Mínima distorção.
    - Qualidade dos detalhes.

    #align(bottom)[
      Fonte: #cite_prose(<pacelli:2025:detection_and_segmentation>).
      #v(32pt)
    ]
  ],
  [
    #image(
      width: 448pt,
      "../assets/images/cbct.png",
    )
  ],
)

#colbreak()

#grid(
  align: (top, horizon),
  columns: (1fr, auto),
  rows: 1fr,
  gutter: 16pt,

  [
    #header_2_formatting[Entrada]

    #stress[Radiografia panorâmica]

    #list(
      [Baixo custo, simplicidade.],
      [Dados ocupam menos armazenamento.],
      [Facilidade maior em encontrar datasets.],
    )

    #align(bottom)[
      Fonte e legenda: #cite_prose(<lee:2026:machine_learning_adult_age_estimation>).
      #v(32pt)
    ]
  ],
  [
    #image(
      width: 448pt,
      "../assets/images/radiografia.png",
    )
  ],
)


#title_slide("Trabalhos relacionados")

== #cite_prose(<oliveira:2026:radiografias_odontologicas_grupos_etarios>)#footnote[
  #cite(<oliveira:2026:radiografias_odontologicas_grupos_etarios>, form: "full")
]

#grid(
  columns: (1fr, 2fr),
  gutter: 16pt,
  [
    - #stress[Classificam] em:
      - criança (01 - 14);
      - jovem (15 - 25);
      - adulto (26 - 99).
  ],
  [
    - Montaram um banco de 1545 #stress[radiografias] panorâmicas (1 a 91 anos)#footnote[
        Universidade Federal do Ceará. Acesso em: #link("https://ageestimationsbcas2026.github.io/Age-estimation-from-panoramic-dental-radiographs/").
      ].
    - *Entrada:* imagem, idade, sexo, condição de cada dente #text(fill: black.lighten(30%))[(presente, ausente, incluso, radicular, implante, traumatismo)].
  ],
)

#pagebreak()

== #cite_prose(<lee:2026:machine_learning_adult_age_estimation>)#footnote[
  #cite(<lee:2026:machine_learning_adult_age_estimation>, form: "full")
]


- #stress[Regressão] por @ml. Comparado com regressão linear convencional.
- Montaram um banco de 2415 #stress[radiografias] panorâmicas (20 a 90 anos)#footnote[
    Universidade Católica da Coreia, Hospital St. Mary de Seul. Solicitamos o banco aos autores.
  ].
- *Entrada:* imagem, idade, sexo, condições de cada dente #text(fill: black.lighten(30%))[(hígido, ausente, impactado, defeito, raiz residual, canal, restauração, prótese, implante)]#footnote[Pode registrar uma, ou duas características, caso o dente apresente ambas.].
