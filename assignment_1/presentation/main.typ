#import "packages.typ": glossarium, polylux, quati-abnt
#import "components.typ": cover_page, page_footer, page_progress_bar, slide
#import "style.typ": large_leading, leading, small_leading, theme_color


// ## Layout. Leiaute.
#set text(
  font: "Atkinson Hyperlegible Next",
  size: leading,
)
#show heading: set block(below: large_leading)
#set page(
  paper: "presentation-16-9",
  margin: (bottom: large_leading, rest: leading),
  footer: align(right, page_footer),
  background: align(bottom, page_progress_bar),
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

  #lorem(100)

]


#slide[
  = My first slide

  Here come my three favourite fonts:

  + Atkinson Hyperlegible
  + Alegreya
  + TeX Gyre Pagella

]
