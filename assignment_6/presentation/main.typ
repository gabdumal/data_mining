#import "packages.typ": *
#import "components.typ": *
#import "template.typ": *


// ## Layout. Leiaute.
#show: it => template(it)
#show: it => quati-abnt.link.template(
  it,
  // Define the color of links and cross-references.
  // Defina a cor dos links e das referências cruzadas.
  color_of_links: theme_color,
)
#show: it => quati-abnt.bibliography.template(it)
#show: it => quati-abnt.footnote.template(it)


// ## Content. Conteúdo.

#cover_slide

#include "content/main.typ"

#title_slide("Referências")
#bibliography(
  title: none,
  "data/bibliography.bib",
)

#focus_slide[
  #set text(
    size: larger_leading,
  )

  Agradecemos pela atenção!

  #text(leading)[
    Este trabalho recebeu apoio da Fundação de Amparo à Pesquisa do Estado de Minas Gerais (FAPEMIG).
  ]
]
