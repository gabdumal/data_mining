#import "../packages.typ": *
#import "../components.typ": *
#import "../template.typ": *


#title_slide("Problema")

== Cenário

A estimação da #stress[idade] com base dos *dentes* é comum nas áreas de investigação *forense*, de identificação de pessoas, e de planejamento para tratamento odontológico#footnote[
  #cite(<lee:2026:machine_learning_adult_age_estimation>, form: "full")
].


As mudanças #stress[características] de idade são mais perceptíveis em crianças e jovens do que em *adultos*, o que dificulta a exatidão da estimativa aferida por técnicos humanos.

#pagebreak()

== Técnicas

Em adultos, #stress[características] de interesse incluem:
- quantidade de dentes presentes e de implantes;
- nível de *desgaste* e restaurações;
- condições gerais de saúde.

Métodos #stress[estatísticos] convencionais requerem trabalho de aferência do *técnico* odontológico, e levam a distorções.

#pagebreak()

== Objetivo

Empregar métodos de #stress[mineração de dados] para predizer a *idade* de humanos, com foco em *adultos*.

Utilizar #stress[entradas] de *dados* que requeiram *menor intervenção* física e interpretação por profissionais odontológicos.

Realizar as manipulações de formas não invasivas, e que permitam *preservar* os dentes.

#title_slide("Base de dados")

== Coleta

O #glossarium.gls("inredd", link: false) da #glossarium.gls("usp", link: false) Campus Ribeirão Preto montou a base de dados #stress[InReDD-Dataset-PAN924]#footnote[
  #cite(<costa:2024:dental_digital_dataset_ai>, form: "full")
].

Ela é composta por #strong[924 imagens] de radiografias panorâmicas da população local.

#pagebreak()

== Características

As entradas são compostas por: imagem, sexo, idade, #stress[segmentações].

- As segmentações foram realizadas #strong[manualmente] por especialistas:
  - #strong[Numeração] dos dentes conforme padrão internacional (FDI).
  - Identificação de #stress[características] de interesse acerca de cada dente presente e da boca por inteiro.

- Cada segmentação contém a caixa de delimitação na imagem e uma #stress[categoria] associada.

#pagebreak()

#grid(
  row-gutter: leading / 2,
  strong("Condição da boca"),
  table(
    columns: 4,
    column-gutter: (0pt, small_leading, 0pt),
    [Ed], [Sem dentes], [De], [Dentes presentes],
    [Me], [Maxilar sem dentes], [Mne], [mandíbula sem dentes],
  ),
)

#grid(
  row-gutter: leading / 2,
  strong("Condição de um dente"),
  table(
    columns: 4,
    column-gutter: (0pt, 12pt, 0pt),
    [H], [Saudável], [R], [Restauração],
    [Di], [Desgaste do incisivo], [C], [Cáries],
    [I], [Impactado], [Im], [Implante],
    [M3i], [3º molar impactado], [M3f], [3º molar desenvolvendo],
    [P], [Pôntico], [Dc], [Coroa destruída],
    [Te], [Tratamento endodôntico], [TeM], [Tratamento endodôntico misto],
    [Ri], [Pino intrarradicular], [RiM], [Pino intrarradicular misto],
    [Cp], [Coroa prostética], [CpuM], [Coroa prostética mista],
    [Rr], [Raiz residual],
  ),
)

#pagebreak()

== Abordagem

- #stress[Problema:] essas categorizações não estão relacionadas;
  - não é possível saber que o procedimento #strong[X] foi feito no dente #strong[N].

- #stress[Transformação] dos dados de segmentação.
  - Condição da boca se tornou um atributo categórico (4 classes).
  - #strong[Contagem] das ocorrências de cada condição dental em dado\ paciente (17 características).

- #stress[Classes-objetivo:] transformação da idade em faixas etárias.
  - 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70+

#pagebreak()

#grid(
  columns: (1fr, auto),
  rows: (1fr, auto),
  gutter: small_leading,

  grid.cell(
    align: center + horizon,
    image(
      width: 19cm,
      "../assets/images/segmentacoes_120-M-48.png",
    ),
  ),

  align(horizon)[
    - Idade: 48
    - Faixa: 40-49
    - Sexo: Masculino
    - Boca: Dentes\ presentes (De)
    - #text(fill: color.rgb("999900"))[Saudável (H)]: 14
    - #text(fill: color.rgb("009999"))[Restauração (R)]: 10
    - #text(fill: color.rgb("#009900"))[Tratamento\ endodôntico (Te)]: 3
    - #text(fill: color.rgb("#EE6600"))[Cáries (C)]: 1
  ],

  align(bottom + center)[
    Fonte: #cite_prose(<costa:2024:dental_digital_dataset_ai>).
  ],
)

#pagebreak()
