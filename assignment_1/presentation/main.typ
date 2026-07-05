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
  margin: (y: larger_leading, x: leading),
  footer: align(right, page_footer),
  foreground: align(bottom, page_progress_bar),
  header: align(right, text(weight: "semibold", fill: theme_color)[#toolbox.current-section]),
)


#cover_slide

#toolbox.register-section("Regras de associação")
#focus_slide([
  = #toolbox.current-section
])
#slide[
  == Banana

]

#toolbox.register-section("Agrupamento")
#focus_slide([
  = #toolbox.current-section
])
#slide[
  = Banana

]

#toolbox.register-section("Regressão")
#focus_slide([
  = #toolbox.current-section
])
#slide[
  = Banana

]

#toolbox.register-section("Classificação")
#focus_slide([
  = #toolbox.current-section
])
#slide[
  = Banana

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
