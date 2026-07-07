#import "packages.typ": *
#import "components.typ": *
#import "template.typ": *


// ## Layout. Leiaute.
#show: it => template(it)

#let color_of_links = theme_color

// ## Links. Ligações.
#show link: it => {
  // TODO: use if type(it.dest) != label
  if (color_of_links != none) {
    set text(fill: color_of_links)
    it
  } else {
    it
  }
}

// ## Citations. Citações.
#show cite: it => {
  if (color_of_links != none) {
    set text(fill: color_of_links)
    it
  } else {
    it
  }
}

// ## References. Referências.
#show ref: it => {
  // NBR 6024:2012.
  let content = if (color_of_links != none) {
    set text(fill: color_of_links)
    it
  } else {
    it
  }

  content
}

#cover_slide

#include "content/main.typ"

#focus_slide[
  #set text(
    size: larger_leading,
  )

  Agradecemos pela atenção!

  #text(leading)[
    Este trabalho recebeu apoio da Fundação de Amparo à Pesquisa do Estado de Minas Gerais (FAPEMIG).
  ]
]

#bibliography(
  "data/bibliography.bib",
  title: "Referências",
  style: "style/bibliography_style.csl",
)
