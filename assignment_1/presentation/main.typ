#import "packages.typ": *
#import "components.typ": *
#import "style.typ": larger_leading, leading, small_leading, theme_color


// ## Layout. Leiaute.
#set text(
  font: "Atkinson Hyperlegible Next",
  size: leading,
)
#show heading: set block(below: larger_leading)
#set page(
  paper: "presentation-16-9",
  margin: (bottom: larger_leading, rest: leading),
  footer: align(right, page_footer),
  foreground: align(bottom, page_progress_bar),
)


#cover_page

#slide[
  = My first slide

  Here come my three favourite fonts:

  + Atkinson Hyperlegible
  + Alegreya
  + TeX Gyre Pagella

]


#slide[
  = My first slide

  Here come my three favourite fonts:

  + Atkinson Hyperlegible
  + Alegreya
  + TeX Gyre Pagella

]


#focus_page[
  Agradecemos pela atenção!

  #text(leading)[
    Este trabalho recebeu apoio da Fundação de Amparo à Pesquisa do Estado de Minas Gerais (FAPEMIG).
  ]
]
