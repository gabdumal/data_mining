// # Components. Componentes.

#import "data/data.typ": authors, date, subtitle, title
#import "packages.typ": (
  polylux.alternatives, polylux.alternatives-cases, polylux.alternatives-fn, polylux.alternatives-match,
  polylux.enable-handout-mode, polylux.item-by-item, polylux.later, polylux.one-by-one, polylux.only,
  polylux.reveal-code, polylux.slide, polylux.toolbox, polylux.uncover, quati-abnt.common.components,
  quati-abnt.common.components.cite_prose, quati-abnt.common.components.closed_discussion_note,
  quati-abnt.common.components.create_status_note, quati-abnt.common.components.describe_figure,
  quati-abnt.common.components.done_note, quati-abnt.common.components.editor_note,
  quati-abnt.common.components.equation, quati-abnt.common.components.format_table,
  quati-abnt.common.components.open_discussion_note, quati-abnt.common.components.progress_note,
  quati-abnt.common.components.todo_note,
)
#import "style.typ": large_leading, larger_leading, leading, small_leading, theme_color


// ## Page. Página.

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

#let cover_slide = slide[
  #set page(
    header: none,
    footer: none,
    foreground: none,
    margin: leading,
  )

  #grid(
    columns: (1fr, auto),
    align: (left, right),
    [
      #text(
        fill: theme_color,
        weight: "bold",
        size: larger_leading,
        title,
      )\
      #text(
        size: large_leading,
        subtitle,
      )

      #date.display("[day]/[month]/[year]")

      #(
        authors
          .map(author => [#(
              (
                author.first_name,
                author.middle_name,
                author.last_name,
              )
                .filter(name => name != none)
                .join(" ")
            )#footnote(text(small_leading, author.curriculum))])
          .join(", ")
      )
    ],
    [
      #image(
        "/assets/images/brasao_ufjf.png",
        width: 5cm,
      )
    ],
  )
]

#let focus_slide = it => slide[
  #set page(
    header: none,
    footer: none,
    foreground: none,
    margin: leading,
    fill: theme_color,
  )
  #set align(center + horizon)
  #set text(
    fill: white,
    weight: "black",
    size: larger_leading,
  )
  #show heading.where(
    level: 1,
  ): set text(
    size: larger_leading,
  )

  #it
]


// ## Note. Nota.

#let review_note = (
  prefixes: none,
  it,
) => {
  let color = oklch(82.01%, 0.159, 323.15deg)
  create_status_note(
    fill: color,
    prefixes: prefixes,
    status: "REVISAR",
    stroke: color.saturate(50%),
    it,
  )
}

#let note_from_gabriel = (
  note: editor_note,
  it,
) => {
  let color = oklch(80.43%, 0.1, 278.25deg)
  note(
    prefixes: (
      (
        body: "Gabriel",
        fill: color,
        stroke: color.saturate(25%),
      ),
    ),
    it,
  )
}
