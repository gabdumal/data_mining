#import "components.typ": toolbox
#import "packages.typ": hydra
#import "style/style.typ": larger_leading, leading, small_leading, theme_color

#let page_footer = text(size: small_leading)[#toolbox.slide-number / #toolbox.last-slide-number]

#let page_progress_bar = {
  let height = 4pt
  toolbox.progress-ratio(ratio => {
    stack(
      dir: ltr,
      rect(stroke: none, fill: theme_color, height: height, width: ratio * 100%),
      rect(stroke: none, fill: none, height: height, width: (1 - ratio) * 100%),
    )
  })
}

#let template = it => {
  set text(
    font: "Atkinson Hyperlegible Next",
    size: leading,
  )
  show heading: set block(below: larger_leading)
  set page(
    paper: "presentation-16-9",
    margin: (y: larger_leading, x: leading),
    footer: align(right, page_footer),
    foreground: align(bottom, page_progress_bar),
    header: context align(
      right,
      text(
        weight: "semibold",
        fill: theme_color,
        hydra(1),
      ),
    ),
  )
  it
}
