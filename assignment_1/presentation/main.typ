#import "packages.typ": *
#import "components.typ": *
#import "template.typ": *


// ## Layout. Leiaute.
#show: it => template(it)

#cover_slide

#title_slide("Regras de associação")

#slide[
  == Banana

]

#title_slide("Agrupamento")
#slide[
  == Banana

]

#title_slide("Regressão")
#slide[
  == Banana

]

#title_slide("Classificação")
#slide[
  == Banana

]

#focus_slide[
  #set text(
    size: larger_leading,
  )

  Agradecemos pela atenção!

  #text(leading)[
    Este trabalho recebeu apoio da Fundação de Amparo à Pesquisa do Estado de Minas Gerais (FAPEMIG).
  ]
]
